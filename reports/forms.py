from django import forms
from docs.models import *
from bootstrap_datepicker_plus import DatePickerInput, MonthPickerInput
from django.forms import Select


class ContragentModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class MaterialsModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name

class ReceiptModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class CameFilterForm(forms.Form):
    min_data = forms.DateField(required=False, label='Начальная дата', widget=DatePickerInput(attrs={'id': 'datepicker'}, options={"format": "DD.MM.YYYY",
                                                                                                                   "locale": "ru"}))
    max_data = forms.DateField(required=False, label='Конечная дата',
                               widget=DatePickerInput(attrs={'id': 'datepicker'}, options={"format": "DD.MM.YYYY", "locale": "ru"}))
    contragent = ContragentModelChoiceField(required=False, label='Контрагент', queryset=Contragents.objects.all(), widget=Select(attrs={'class':
                                                                                                                                             'form-control'}))
    material = ContragentModelChoiceField(required=False, label='Материал', queryset=Materials.objects.all(), widget=Select(attrs={'class': 'form-control'}))

class ReceiptFilterForm(forms.Form):
    data = forms.DateField(required=False, label='Месяц', widget=MonthPickerInput(attrs={'id': 'datepicker'}, options={"locale": "ru"}))
    receipt = ReceiptModelChoiceField(required=False, label='Рецепт', queryset=Receipt.objects.all(), widget=Select(attrs={'class': 'form-control'}))