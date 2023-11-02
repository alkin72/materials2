from itertools import chain
from operator import attrgetter

import django
from django.shortcuts import render
from .forms import CameFilterForm
from docs.models import *
from django.db.models import Sum, Count
from django.views.generic.base import View

from wkhtmltopdf.views import PDFTemplateResponse



# def getpdf(request):
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="file.pdf"'
#     p = canvas.Canvas(response)
#     p.setFont("Times-Roman", 55)
#     p.drawString(100,700, "Hello, Javapoint.")
#     p.showPage()
#     p.save()
#     return response

class PDFView(View):
    template = 'reports/came.html'

    def get(self, request):
        data = {"mydata": "your data"}  # data that has to be renderd to pdf templete
        response = PDFTemplateResponse(request=request,
                                       template=self.template,
                                       filename="hello.pdf",
                                       context=data,
                                       show_content_in_browser=False,
                                       cmd_options={'margin-top': 10,
                                                    "zoom": 1,
                                                    "viewport-size": "1366 x 513",
                                                    'javascript-delay': 1000,
                                                    'footer-center': '[page]/[topage]',
                                                    "no-stop-slow-scripts": True},
                                       )
        return response


# @ login_required()
def reports_journal(request):
    rem = RegisterMaterialsMove.objects.all()
    data = {'title': 'Журнал Отчетов',
            'system_info': 'Дата создания: 25.12.2021 12:00, Контрагент: ООО "", Создан',
            'rem': rem
            }
    return render(request, 'reports/reports_journal.html', data)


def expense(request):
    exp = RegisterMaterialsMove.objects.filter(move=False)
    registrator = Document.objects.filter(category_move=False)

    form = CameFilterForm(request.GET)
    if form.is_valid():
        if form.cleaned_data['min_data']:
            exp = exp.filter(datetime__gte=form.cleaned_data['min_data'])
        if form.cleaned_data['max_data']:
            exp = exp.filter(datetime__lte=form.cleaned_data['max_data'])
        if form.cleaned_data['contragent']:
            registrator = registrator.filter(contragent=form.cleaned_data['contragent'])
            exp = exp.filter(registrator__in=registrator)
        if form.cleaned_data['material']:
            exp = exp.filter(materials=form.cleaned_data['material'])

    sum = exp.aggregate(Sum=Sum('value'))
    count = exp.count()
    data = {'title': 'Отчет по расходу материала',
            'system_info': 'Расход за весь период по датам',
            'exp': exp,
            'form': form,
            'sum': sum,
            'count': count
            }
    return django.shortcuts.render(request, 'reports/expense.html', data)


def came(request):
    came = RegisterMaterialsMove.objects.filter(move=True)
    registrator = Document.objects.filter(category_move=True)
    material_search = Materials.objects.all()
    form = CameFilterForm(request.GET)
    if form.is_valid():
        if form.cleaned_data['min_data']:
            came = came.filter(datetime__gte=form.cleaned_data['min_data'])
        if form.cleaned_data['max_data']:
            came = came.filter(datetime__lte=form.cleaned_data['max_data'])
        if form.cleaned_data['contragent']:
            registrator = registrator.filter(contragent=form.cleaned_data['contragent'])
            came = came.filter(registrator__in=registrator)
        if form.cleaned_data['material']:
            came = came.filter(materials=form.cleaned_data['material'])

    sum = came.aggregate(Sum=Sum('value'))
    count = came.count()
    data = {'title': 'Отчет по приходу материала',
            'system_info': 'Приход за весь период по датам',
            'came': came,
            'form': form,
            'sum': sum,
            'count': count
            }
    return django.shortcuts.render(request, 'reports/came.html', data)


# журнал заявок==============================================================
def remainder(request):
    lst = []
    dublicates = RegisterMaterialsRemainder.objects.values('materials').annotate(count=Count('materials')).filter(count__gt=1)
    non_dublicates = RegisterMaterialsRemainder.objects.values('materials').annotate(count=Count('materials')).filter(count=1)
    # ls = RegisterMaterialsRemainder.objects.all().values_list('materials', flat=True).distinct().order_by('materials')
    #rem = RegisterMaterialsRemainder.objects.filter().exclude(value=0).order_by('materials', '-datetime').distinct()#.distinct('materials')
    #rem1 = RegisterMaterialsRemainder.objects.order_by('materials')
    records_dub = RegisterMaterialsRemainder.objects.filter(materials__in=[item['materials']for item in dublicates]).order_by('materials', '-datetime')
    records_nondub = RegisterMaterialsRemainder.objects.filter(materials__in=[item['materials']for item in non_dublicates])
    tmp = ''
    for i in records_dub:
        if i.materials != tmp:
            lst.append(i)
            tmp = i.materials
    rem = sorted(chain(records_nondub, lst), key=attrgetter('datetime'), reverse=True)
    remainder_list = rem
    data = {'title': 'Остатки материала',
            'system_info': 'Дата создания: 25.12.2021 12:00, Контрагент: ООО "", Проведен',
            'remainder': remainder_list,
            }
    return django.shortcuts.render(request, 'reports/remainder.html', data)
# конец журнал заявок ======================================================
