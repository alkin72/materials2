import calendar
import itertools as it
import decimal
import datetime
from django.db.models import Sum
from docs.models import *
from . import forms


class Move:

    @staticmethod
    def calculate_receipt(value, rec, date):
        list_ = []
        closest_date = ''
        lowest_time_delta = 99999999
        reg_rec = ''
        # receipt_det = ReceiptDetail.objects.filter(receipt=rec)
        register_rec = RegisterReceipt.objects.filter(receipt=rec).order_by('-datetime')
        for r in register_rec:
            current_time_delta = abs((r.datetime - date).total_seconds())
            if current_time_delta < lowest_time_delta:
                closest_date = r.datetime
                reg_rec = r
                lowest_time_delta = current_time_delta
        reg = RegisterReceiptComposition.objects.filter(register_receipt=reg_rec, datetime=closest_date)
        for item in reg:
            coef = item.materials.coeficient.value
            value_mat = 0
            value_mat = decimal.Decimal(value * (item.value/100)*coef).quantize(decimal.Decimal('1.000'))  # рассчитываем кол-во материала по
            # процентам по
            # рецепту
            list_.append({'materials': item.materials_id, 'value': value_mat, 'unit': 2})
        return list_

    @staticmethod
    def move_receipt(pk, date):  # расчет и сохранение списания по заявкам по рецепту
        list_ = []
        list_rec = []
        doc = forms.DocumentReceipt.objects.get(pk=pk)  # получаем документ заявки
        doc_rec_ref = DocumentReceiptRef.objects.filter(doc_receipt=doc)  # получаем список рецептов по заявке
        unit = 0
        for i in doc_rec_ref:
            list_rec.append(i.receipt)
            list_.append(Move.calculate_receipt(i.value, i.receipt, doc.datetime))
            unit = i.unit.unit_id
        # list_reg_rec = RegisterReceipt.objects.filter(receipt_in=doc_rec_ref)
        # comp = 0
        # if date <= list_reg_rec:
        #     comp = RegisterReceiptComposition.objects.filter(register_receipt__in=list_reg_rec.register_receipt_id)
        # doc_rec = forms.DocumentReceiptRef.objects.filter(doc_receipt_id=pk)
        lst = sum(list_, [])
        d = {}
        key = lambda x: x['materials']  # суммирование значений одинакового материала и объединение
        groups = it.groupby(sorted(lst, key=key), key)
        result = [{'materials': k, 'value': sum(x['value'] for x in g), 'unit': 2} for k, g in groups]
        return result

    @staticmethod
    def un_move(pk):
        DocumentReceipt.objects.filter(pk=pk).update(move=False)

    @staticmethod
    def move_document(pk, move_deff):
        doc = forms.Document.objects.get(pk=pk)     # документ получили
        # ref_dict - агрегируем полученные данные таблицы
        # ref_dict = forms.DocumentRef.objects.filter(doc_id=doc.doc_id).values('materials').annotate(value=Sum('value')).order_by('materials')
        # ref - фильтруем записи в таблице ссылке
        ref = forms.DocumentRef.objects.filter(doc_id=doc.doc_id)
        date = doc.datetime     # сохраняем дату документа
        # month - последний день месяца документа
        month = datetime.date(date.year, date.month, 1) + datetime.timedelta(days=calendar.monthrange(date.year, date.month)[1] - 1)    # последняя дата
        # месяца текущего документа1
        r = RegisterMaterialsMove.objects.filter(registrator=pk)    # получаем данные в таблице materials_move (существуют или нет)

        if doc.move:    # если док проведен, то
            Document.objects.filter(pk=pk).update(move=False)   # обновляем значение проводки в документе на False
            if r:   # если есть записи в materials_move, то
                Move.move_remainder(False, r, month, doc.category_move)     # удаляем записи из остатков и пересчитываем остатки по таблице
                r.delete()   # удаляем записи в materials_move
        else:   # если док не проведен, то
            Document.objects.filter(pk=pk).update(move=True)    # обновляем значение проводки в документе на True
            for item in ref:    # пробегаем по записям документа и создаем их в materials_move
                RegisterMaterialsMove.objects.create(materials=item.materials, value=item.value, datetime=doc.datetime, registrator=doc,
                                                     move=doc.category_move, action=True, move_deff=move_deff)
            r = RegisterMaterialsMove.objects.filter(registrator=pk)  # получаем данные в таблице materials_move (существуют или нет)
            Move.move_remainder(True, r, month, doc.category_move)  # добавляем записи в остатках и пересчитываем остатки по таблице

    @staticmethod
    def move_remainder(move, r, month, category):   # обработка таблицы остатков
        r = r.values('materials').annotate(value=Sum('value')).order_by('materials')    # r - агрегируем полученные данные из materials_move
        rem = RegisterMaterialsRemainder.objects.filter(datetime=month)     # получаем данные из остатков по последнему дню месяца документа
        Move.calculate_current(rem, r, move, category, month)
        # проводка
        # if move:    # если проводка, то
            # if category:    # если приход, то
          #  Move.calculate_current(rem, r, True, category, month)
            # else:   # если расход, то
            #     Move.calculate_current(rem, r, True, category, month)
            #     pass

        # отмена проводки
        #else:   # если отмена проводки, то
            # if category:    # если приход, то
         #   Move.calculate_current(rem, r, False, category, month)
            # else:   # если расход, то
            #     Move.calculate_current(rem, r, False, category, month)
            #     pass

    @staticmethod
    def calculate_current(rem, r, direction, category, month):  # rem - список данных из остатков, r - список данных в materials_move,
        # direction - направление(проводка) движения материалов, category - приход расход, month - последняя дата месяца документа
        list_data_materials = RegisterMaterialsRemainder.objects.filter(datetime__lt=month).exclude(value=0)  # список записей остатков предыдущих месяцев
        for i_r in r:
            if list_data_materials.filter(materials_id=i_r['materials']):   # если в списке предыдущих месяцев есть данные по материалу, то
                #   данные по остаткам предыдущие
                rem_last_month = RegisterMaterialsRemainder.objects.filter(datetime__lt=month, materials_id=i_r['materials']).exclude(value=0).order_by(
                    '-datetime').first().value    # order_by('-datetime').first().value
            else:
                rem_last_month = 0

            if rem.filter(materials_id=i_r['materials']):
                for item in rem:
                    if i_r['materials'] == item.materials.materials_id:     # если в остатках есть данные по материалу, то
                        if direction:
                            if category:
                                item.value += i_r['value']
                            else:
                                item.value -= i_r['value']
                        else:
                            if category:
                                item.value -= i_r['value']
                            else:
                                item.value += i_r['value']
                        rem.filter(materials=item.materials).update(value=item.value)
                        if item.value == 0:
                            pass
                            # rem.filter(materials=item.materials).delete()
            else:
                if category:
                    if direction:
                        if list_data_materials:
                            i_r['value'] += rem_last_month
                        RegisterMaterialsRemainder.objects.create(materials_id=i_r['materials'], value=i_r['value'], datetime=month)
                    else:
                        if list_data_materials:
                            i_r['value'] -= rem_last_month
                        RegisterMaterialsRemainder.objects.create(materials_id=i_r['materials'], value=-i_r['value'], datetime=month)
                else:
                    if direction:
                        if list_data_materials:
                            i_r['value'] -= rem_last_month
                        RegisterMaterialsRemainder.objects.create(materials_id=i_r['materials'], value=-i_r['value'], datetime=month)
                    else:
                        if list_data_materials:
                            i_r['value'] += rem_last_month
                        RegisterMaterialsRemainder.objects.create(materials_id=i_r['materials'], value=i_r['value'], datetime=month)
        Move.calculate(r, direction, category, month)

    @staticmethod
    def calculate(r, direction, category, month):   # r - список данных в materials_move,
        # direction - направление(проводка) движения материалов, category - приход расход, month - последняя дата месяца документа
        month_next = datetime.datetime(month.year, month.month, 1) + datetime.timedelta(days=calendar.monthrange(month.year, month.month)[1])
        rem = RegisterMaterialsRemainder.objects.filter(datetime__range=[month_next, '3000-01-01']) # получаем все последующие записи

        for item in rem:
            if item.datetime > month:
                if category:
                    if direction:
                        for i_r in r:
                            if item.materials.materials_id == i_r['materials']:
                                item.value += i_r['value']
                                rem.filter(register_materials_remainder_id=item.register_materials_remainder_id).update(
                                    value=item.value)
                    else:
                        for i_r in r:
                            if item.materials.materials_id == i_r['materials']:
                                item.value -= i_r['value']
                                rem.filter(register_materials_remainder_id=item.register_materials_remainder_id).update(
                                    value=item.value)  # rem.filter(materials=item.materials).update(value=item.value)
                        if item.value == 0:
                            pass
                            # rem.filter(materials=item.materials).delete()
                else:
                    if direction:
                        for i_r in r:
                            if item.materials.materials_id == i_r['materials']:
                                item.value -= i_r['value']
                                rem.filter(register_materials_remainder_id=item.register_materials_remainder_id).update(
                                    value=item.value)
                    else:
                        for i_r in r:
                            if item.materials.materials_id == i_r['materials']:
                                item.value += i_r['value']
                                rem.filter(register_materials_remainder_id=item.register_materials_remainder_id).update(
                                    value=item.value)