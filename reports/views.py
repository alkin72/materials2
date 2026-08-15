import datetime
from itertools import chain
from operator import attrgetter
import os
import django
from django.http import HttpResponse
from django.shortcuts import render
from .forms import CameFilterForm, ReceiptFilterForm
from docs.models import *
from django.db.models import Sum, Count
from django.conf import settings

# Импорты для ReportLab
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Регистрация кириллического шрифта
try:
    # Учитываем папку "DejaVu Sans" в пути
    font_path = os.path.join(settings.BASE_DIR, 'reports', 'static', 'reports', 'fonts', 'DejaVu Sans', 'DejaVuSans.ttf')
    pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))
    DEFAULT_FONT = 'DejaVuSans'
except Exception as e:
    print(f"Ошибка загрузки шрифта: {e}")
    DEFAULT_FONT = 'Helvetica'

max_data = None
min_data = None
contragent_pdf = None
material = None
title = None
move = True
receipt_find = None

def generate_pdf(request):
    """Создание PDF с помощью ReportLab."""
    global material, min_data, max_data, contragent_pdf, title, move
    con = None
    
    if move:
        came = RegisterMaterialsMove.objects.filter(move=True)
        registrator = Document.objects.filter(category_move=True)
    else:
        came = RegisterMaterialsMove.objects.filter(move=False)
        registrator = Document.objects.filter(category_move=False)

    form = CameFilterForm(request.POST)
    if form.is_valid():
        if min_data:
            came = came.filter(datetime__gte=min_data)
        if max_data:
            came = came.filter(datetime__lte=max_data)
        if contragent_pdf:
            registrator = registrator.filter(contragent=contragent_pdf)
            came = came.filter(registrator__in=registrator)
        if material:
            came = came.filter(materials=material)
        if contragent_pdf:
            con = contragent_pdf.name

    sum_val = came.aggregate(Sum=Sum('value'))['Sum']
    sum_total = round(sum_val, 2) if sum_val is not None else 0.0
    count = came.count()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=report.pdf'

    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontName=DEFAULT_FONT, fontSize=16, spaceAfter=10)
    normal_style = ParagraphStyle('NormalStyle', parent=styles['Normal'], fontName=DEFAULT_FONT, fontSize=10)
    
    story = []
    doc_title = title if title else "Отчет"
    story.append(Paragraph(doc_title, title_style))
    story.append(Paragraph("Системная информация: за весь период по датам", normal_style))
    story.append(Paragraph(f"Дата начала: {min_data or '-'}", normal_style))
    story.append(Paragraph(f"Дата конец: {max_data or '-'}", normal_style))
    story.append(Paragraph(f"Контрагент: {con or '-'}", normal_style))
    story.append(Paragraph(f"Материал: {material or '-'}", normal_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph(f"<b>Количество записей:</b> {count} | <b>Сумма материала:</b> {sum_total}", normal_style))
    story.append(Spacer(1, 15))

    table_data = [["Дата", "Материал", "Значение"]]
    for el in came:
        table_data.append([str(el.datetime), str(el.materials), str(el.value)])

    t = Table(table_data, colWidths=[150, 250, 100])
    t.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), DEFAULT_FONT),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t)

    doc.build(story)

    material = contragent_pdf = min_data = max_data = con = title = None
    move = True

    return response


def remainder(request):
    """Отчет по остаткам материала."""
    global title
    rem = RegisterMaterialsMove.objects.all()
    title = 'Отчет по остаткам материала'
    data = {
        'title': title,
        'system_info': 'Остатки за весь период по датам',
        'rem': rem
    }
    return render(request, 'reports/remainder.html', data)


def reports_journal(request):
    """Журнал отчетов."""
    rem = RegisterMaterialsMove.objects.all()
    data = {
        'title': 'Журнал Отчетов',
        'system_info': 'Дата создания: 25.12.2021 12:00, Контрагент: ООО "", Создан',
        'rem': rem
    }
    return render(request, 'reports/reports_journal.html', data)


def generate_pdf_rec(request):
    """Создание PDF рецептов с подчинёнными записями с помощью ReportLab."""
    global receipt_find, min_data, max_data, contragent_pdf, title
    reg_receipt = RegisterReceipt.objects.all()
    reg_rec_comp = RegisterReceiptComposition.objects.all()

    form = ReceiptFilterForm(request.GET)
    if form.is_valid():
        if min_data:
            reg_receipt = reg_receipt.filter(datetime__gte=min_data)
        if max_data:
            reg_receipt = reg_receipt.filter(datetime__lte=max_data)
        if receipt_find:
            reg_receipt = reg_receipt.filter(receipt=receipt_find)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=receipt_report.pdf'

    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()
    normal_style = ParagraphStyle('NormalStyle', parent=styles['Normal'], fontName=DEFAULT_FONT, fontSize=10)
    bold_style = ParagraphStyle('BoldStyle', parent=styles['Normal'], fontName=DEFAULT_FONT, fontSize=10, fontNameEnc='utf-8')

    story = [Paragraph("Отчет по рецептам с составом", ParagraphStyle('H1', parent=styles['Heading1'], fontName=DEFAULT_FONT))]
    story.append(Paragraph(f"Количество документов: {reg_receipt.count()}", normal_style))
    story.append(Spacer(1, 15))

    # Формируем структуру таблицы, включая подчинённые записи
    # Колонки: Документ / ID, Дата / Компонент, Рецепт / Значение
    table_data = [["ID / Рецепт", "Дата / Состав", "Детали / Значение"]]
    
    for el in reg_receipt:
        # Строка самого документа (шапка для группы подчинённых записей)
        table_data.append([f"Документ ID: {el.pk}", str(el.datetime), f"Рецепт: {el.receipt}"])
        
        # Ищем подчинённые записи для текущего документа (предполагаем поле связи, например, registrator или receipt)
        # Замените 'registrator' или 'receipt' на реальное имя связи в RegisterReceiptComposition из models.py, если оно отличается
        children = reg_rec_comp.filter(register_receipt=el) # или .filter(receipt=el.receipt)
        
        if children.exists():
            table_data.append(["--- Состав:", "Компонент / Материал", "Количество / Значение"])
            for comp in children:
                table_data.append(["", str(comp.materials if hasattr(comp, 'materials') else comp), str(comp.value if hasattr(comp, 'value') else "")])
        else:
            table_data.append(["", "Нет подчинённых записей", ""])

    t = Table(table_data, colWidths=[120, 200, 180])
    t.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), DEFAULT_FONT),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t)

    doc.build(story)
    min_data = max_data = receipt_find = None

    return response


def expense(request):
    """Отчет по расходу материала."""
    global material, min_data, max_data, contragent_pdf, title, move
    exp = RegisterMaterialsMove.objects.filter(move=False)
    registrator = Document.objects.filter(category_move=False)
    form = CameFilterForm(request.GET)
    if form.is_valid():
        if form.cleaned_data.get('min_data'):
            min_data = form.cleaned_data['min_data']
            exp = exp.filter(datetime__gte=form.cleaned_data['min_data'])
        if form.cleaned_data.get('max_data'):
            max_data = form.cleaned_data['max_data']
            exp = exp.filter(datetime__lte=form.cleaned_data['max_data'])
        if form.cleaned_data.get('contragent'):
            contragent_pdf = form.cleaned_data['contragent']
            registrator = registrator.filter(contragent=form.cleaned_data['contragent'])
            exp = exp.filter(registrator__in=registrator)
        if form.cleaned_data.get('material'):
            material = form.cleaned_data['material']
            exp = exp.filter(materials=form.cleaned_data['material'])
    title = 'Отчет по расходу материала'
    move = False
    sum_val = exp.aggregate(Sum=Sum('value'))['Sum']
    sum_total = round(sum_val, 2) if sum_val is not None else 0.0
    count = exp.count()
    data = {
        'title': title,
        'system_info': 'Расход за весь период по датам',
        'exp': exp,
        'form': form,
        'sum': {'Sum': sum_total},
        'count': count
    }
    return render(request, 'reports/expense.html', data)


def receipt_data(request):
    """Изменения рецептов по датам."""
    global receipt_find, min_data, max_data, contragent_pdf, title
    lst = []
    reg_receipt = RegisterReceipt.objects.all()
    reg_rec_comp = RegisterReceiptComposition.objects.all()
    form = ReceiptFilterForm(request.GET)
    if form.is_valid():
        if form.cleaned_data.get('min_data'):
            min_data = form.cleaned_data['min_data']
            reg_receipt = reg_receipt.filter(datetime__gte=form.cleaned_data['min_data'])
        if form.cleaned_data.get('max_data'):
            max_data = form.cleaned_data['max_data']
            reg_receipt = reg_receipt.filter(datetime__lte=form.cleaned_data['max_data'])
        if form.cleaned_data.get('receipt'):
            receipt_find = form.cleaned_data['receipt']
            reg_receipt = reg_receipt.filter(receipt=form.cleaned_data['receipt'])
            for i in reg_receipt:
                lst += list(reg_rec_comp.filter(register_receipt=i))
            reg_rec_comp = lst
    title = 'Изменения рецептов по датам'
    count = reg_receipt.count()
    data = {
        'title': title,
        'system_info': 'за весь месяц',
        'rec': reg_receipt,
        'reg': reg_rec_comp,
        'form': form,
        'count': count
    }
    return render(request, 'reports/receipt_data.html', data)


def came(request):
    """Отчет по приходу материала."""
    global material, min_data, max_data, contragent_pdf, title, move
    move = True
    c_data = RegisterMaterialsMove.objects.filter(move=True)
    registrator = Document.objects.filter(category_move=True)
    form = CameFilterForm(request.GET)
    if form.is_valid():
        if form.cleaned_data.get('min_data'):
            min_data = form.cleaned_data['min_data']
            c_data = c_data.filter(datetime__gte=form.cleaned_data['min_data'])
        if form.cleaned_data.get('max_data'):
            max_data = form.cleaned_data['max_data']
            c_data = c_data.filter(datetime__lte=form.cleaned_data['max_data'])
        if form.cleaned_data.get('contragent'):
            contragent_pdf = form.cleaned_data['contragent']
            registrator = registrator.filter(contragent=form.cleaned_data['contragent'])
            c_data = c_data.filter(registrator__in=registrator)
        if form.cleaned_data.get('material'):
            material = form.cleaned_data['material']
            c_data = c_data.filter(materials=form.cleaned_data['material'])
    title = 'Отчет по приходу материала'
    sum_val = c_data.aggregate(Sum=Sum('value'))['Sum']
    sum_total = round(sum_val, 2) if sum_val is not None else 0.0
    count = c_data.count()
    data = {
        'title': title,
        'system_info': 'Приход за весь период по датам',
        'came': c_data,
        'form': form,
        'sum': {'Sum': sum_total},
        'count': count
    }
    return render(request, 'reports/came.html', data)
