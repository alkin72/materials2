from .models import *
from django import forms
from django.forms import TextInput, Select, CheckboxInput, BooleanField, CharField
from bootstrap_datepicker_plus import DatePickerInput
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset


class ContragentModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.username


class MaterialsModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class UnitModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


# Форма Документа =================================
class DocumentForm(forms.ModelForm):

    contragent = ContragentModelChoiceField(label='Контрагент', queryset=Contragents.objects.all(), widget=Select(attrs={'class': 'form-control'}))
    holding = UserModelChoiceField(label='Пользователь', queryset=AuthUser.objects.all(), widget=Select(attrs={'class': 'form-control'}))
    move = BooleanField(required=False, label='Провести', widget=CheckboxInput(attrs={'class': 'form-check-input'}))
    category_move = forms.ChoiceField(label='Тип документа', choices=CHOICES_category_doc)
    number = CharField(label='Номер', required=False, widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'номер',
                                                                               'readonly': 'readonly'}))
    datetime = forms.DateField(label='Дата', widget=DatePickerInput(attrs={'id': 'datepicker'}, options={"format": "DD.MM.YYYY", "locale": "ru"}))
    #isdelete = BooleanField(label='Пометить на удаление')

    class Meta:
        model = Document
        fields = ('doc_id', 'number', 'datetime', 'holding', 'move', 'category_move', 'contragent', 'note', 'isdelete')
        # exclude = ['user']
        widgets = {
            "hold": Select(attrs={'class': 'form-control', 'placeholder': 'пользователь'}),
            "category_move": CheckboxInput(attrs={'class': 'form-control'}),
            "move": TextInput(attrs={'class': 'form-control'}),
            "note": TextInput(attrs={'class': 'form-control', 'placeholder': 'Примечание'}),
            "con": Select(attrs={'class': 'form-control', 'placeholder': 'контрагент'}),
        }

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_tag = False  # This is crucial.
        helper.layout = Layout(
            Fieldset('Создание документа', 'number', 'datetime', 'holding', 'category_move', 'move', 'contragent'),
        )
        return helper


class DocFormHelper(FormHelper):

    def __init__(self, *args, **kwargs):
        super(DocFormHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.disable_csrf = True
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.layout = Layout(Fieldset("Добавьте строки данных", 'materials', 'value', 'unit',),)


DocumentDetailFormSet = inlineformset_factory(Document, DocumentRef, can_delete=True, fields='__all__', extra=14)

DocFormSet = inlineformset_factory(Document, DocumentRef, can_delete=True, fields='__all__', extra=2)
# Форма Документа конец=================================


# Форма Документа заявки =================================
class DocumentReceptForm(forms.ModelForm):

    contragent = ContragentModelChoiceField(label='Контрагент', queryset=Contragents.objects.all(), widget=Select(attrs={'class': 'form-control'}))
    holding = UserModelChoiceField(label='Пользователь', queryset=AuthUser.objects.all(), widget=Select(attrs={'class': 'form-control'}))
    move = BooleanField(required=False, label='Провести', widget=CheckboxInput(attrs={'class': 'form-check-input'}))
    number = CharField(label='Номер', required=False, widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'номер',
                                                                               'readonly': 'readonly'}))
    datetime = forms.DateField(label='Дата', widget=DatePickerInput(attrs={'id': 'datepicker'}, options={"format": "DD.MM.YYYY", "locale": "ru"}))
    #isdelete = BooleanField(label='Пометить на удаление')

    class Meta:
        model = DocumentReceipt
        fields = ('doc_receipt_id', 'number', 'datetime', 'holding', 'note', 'move', 'contragent', 'isdelete')
        # exclude = ['user']
        widgets = {
            "hold": Select(attrs={'class': 'form-control', 'placeholder': 'пользователь'}),
            "move": TextInput(attrs={'class': 'form-control'}),
            "note": TextInput(attrs={'class': 'form-control', 'placeholder': 'Примечание'}),
            "con": Select(attrs={'class': 'form-control', 'placeholder': 'контрагент'}),
        }

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_tag = False  # This is crucial.
        helper.layout = Layout(
            Fieldset('Создание документа', 'number', 'datetime', 'holding', 'note', 'move', 'contragent'),
        )
        return helper


class DocReceiptFormHelper(FormHelper):

    def __init__(self, *args, **kwargs):
        super(DocReceiptFormHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.disable_csrf = True
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.layout = Layout(Fieldset("Добавьте строки данных", 'receipt', 'value', 'unit',),)


DocumentReceiptDetailFormSet = inlineformset_factory(DocumentReceipt, DocumentReceiptRef, can_delete=True, fields='__all__', extra=6)

DocReceiptFormSet = inlineformset_factory(DocumentReceipt, DocumentReceiptRef, can_delete=True, fields='__all__', extra=2)
# Форма Документа заявки конец =================================