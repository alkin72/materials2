from django import forms
from docs.models import *
from django.forms import TextInput, Select, EmailInput
from bootstrap_datepicker_plus import DatePickerInput
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset


class ContragentForm(forms.ModelForm):
    class Meta:
        model = Contragents
        fields = ('contragents_id', 'name', 'fullname', 'address', 'phone', 'e_mail', 'note')
        labels = {
            'name': 'наименование',
            'fullname': 'полное наименование',
            'address': 'адрес',
            'phone': 'телефон',
            'e_mail': 'e-mail',
            'note': 'примечание',
        }
        widgets = {
            "name": TextInput(attrs={'class': 'form-control', 'placeholder': 'наименование'}),
            "fullname": TextInput(attrs={'class': 'form-control', 'placeholder': 'полное наименование'}),
            "address": TextInput(attrs={'class': 'form-control'}),
            "phone": TextInput(attrs={'class': 'form-control', 'placeholder': 'телефон'}),
            "e_mail": EmailInput(),
            "note": TextInput(attrs={'class': 'form-control'}),
        }


class UnitModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class CategoryModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class CoeficientModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class MaterialsForm(forms.ModelForm):
    category = CategoryModelChoiceField(label='Категория', queryset=Category.objects.all(), widget=Select(attrs={'class': 'form-control'}))
    coeficient = CoeficientModelChoiceField(label='Коэффициент', queryset=Coeficient.objects.all(), widget=Select(attrs={'class': 'form-control'}))
    unit = UnitModelChoiceField(label='Единица измерения', queryset=Unit.objects.all(), widget=Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Materials
        fields = ('materials_id', 'name', 'category', 'coeficient', 'unit')
        labels = {
            'name': 'наименование',
            'category': 'категория' ,
            'coeficient': 'коэффициент списания',
        }
        widgets = {
            "name": TextInput(attrs={'class': 'form-control', 'placeholder': 'наименование'}),
            "category": Select(attrs={'class': 'form-control', 'placeholder': 'категория'}),
            "coeficient": Select(attrs={'class': 'form-control'}),
            "unit": Select(attrs={'class': 'form-control'}),
        }


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('category_id', 'name', 'value', 'note')
        labels = {
            'name': 'наименование',
            'value': 'значение' ,
            'note': 'примечание',
        }
        widgets = {
            "name": TextInput(attrs={'class': 'form-control', 'placeholder': 'наименование'}),
            "value": TextInput(attrs={'class': 'form-control', 'placeholder': 'значение'}),
            "note": TextInput(attrs={'class': 'form-control', 'placeholder': 'примечание'}),
        }


class UnitForm(forms.ModelForm):

    class Meta:
        model = Unit
        fields = ('unit_id', 'name', 'fullname')
        labels = {
            'name': 'наименование',
            'fullname': 'полное наименование' ,
        }
        widgets = {
            "name": TextInput(attrs={'class': 'form-control', 'placeholder': 'наименование'}),
            "fullname": TextInput(attrs={'class': 'form-control', 'placeholder': 'полное наименование'}),
        }


class CoeficientForm(forms.ModelForm):

    class Meta:
        model = Coeficient
        fields = ('coeficient_id', 'name', 'value', 'note')
        labels = {
            'name': 'наименование',
            'value': 'значение' ,
            'note': 'примечание',
        }
        widgets = {
            "name": TextInput(attrs={'class': 'form-control', 'placeholder': 'наименование'}),
            "value": TextInput(attrs={'class': 'form-control', 'placeholder': 'значение'}),
            "note": TextInput(attrs={'class': 'form-control', 'placeholder': 'примечание'}),
        }


class ReceiptForm(forms.ModelForm):

    date = forms.DateField(label='Дата', widget=DatePickerInput(attrs={'id': 'datepicker'}, options={"format": "DD.MM.YYYY", "locale": "ru"}))

    class Meta:
        model = Receipt
        fields = ('receipt_id', 'name', 'date', 'note')
        labels = {
            'name': 'наименование',
            'date': 'дата',
            'note': 'примечание',
        }
        widgets = {
            "name": TextInput(attrs={'class': 'form-control', 'placeholder': 'наименование'}),
            "date": TextInput(attrs={'class': 'form-control', 'placeholder': 'дата'}),
            "note": TextInput(attrs={'class': 'form-control', 'placeholder': 'примечание'}),
        }

        @property
        def helper(self):
            helper = FormHelper()
            helper.form_tag = False  # This is crucial.
            helper.layout = Layout(Fieldset('Создание документа', 'name', 'date', 'note'),)
            return helper


class ReceiptFormHelper(FormHelper):

    def __init__(self, *args, **kwargs):
        super(ReceiptFormHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.layout = Layout(Fieldset("Добавьте строки данных", 'materials', 'value'),)


ReceiptDetailFormSet = inlineformset_factory(Receipt, ReceiptDetail, can_delete=True, fields='__all__', extra=12)

RecFormSet = inlineformset_factory(Receipt, ReceiptDetail, can_delete=True, fields='__all__', extra=2)