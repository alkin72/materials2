import django
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView
from .forms import *
from .utils import *
from . import forms
from django.contrib.auth.decorators import login_required


# @ login_required()
def directory(request):
    data = {'title': 'Справочники',
            'system_info': 'Дата создания: 25.12.2021 12:00, Контрагент: ООО "", Создан'
            }
    return render(request, 'directory/directory.html', data)


def contragents(request):
    contr = forms.Contragents.objects.all()
    data = {'title': 'Журнал контрагентов',
            'system_info': 'Дата создания: 25.12.2021 12:00, Контрагент: ООО "", Проведен',
            'contr': contr,
            }
    return django.shortcuts.render(request, 'directory/contragents.html', data)


def materials(request):
    mat = forms.Materials.objects.all()
    data = {'title': 'Справочник материалов',
            'system_info': 'Дата создания: 25.12.2021 12:00, Контрагент: ООО "", Проведен',
            'mat': mat,
            }
    return django.shortcuts.render(request, 'directory/materials.html', data)


def category(request):
    cat = forms.Category.objects.all()
    data = {'title': 'Справочник категорий материалов',
            'system_info': 'Дата создания: 25.12.2021 12:00, Контрагент: ООО "", Проведен',
            'cat': cat,
            }
    return django.shortcuts.render(request, 'directory/category.html', data)


def unit(request):
    unit = forms.Unit.objects.all()
    data = {'title': 'Справочник единиц измерения',
            'system_info': 'Дата создания: 25.12.2021 12:00, Контрагент: ООО "", Проведен',
            'unit': unit,
            }
    return django.shortcuts.render(request, 'directory/unit.html', data)


def coeficient(request):
    coef = forms.Coeficient.objects.all()
    data = {'title': 'Справочник коффициентов',
            'system_info': 'Дата создания: 25.12.2021 12:00, Контрагент: ООО "", Проведен',
            'coef': coef,
            }
    return django.shortcuts.render(request, 'directory/coeficient.html', data)


def receipt(request):
    r = forms.Receipt.objects.all()
    data = {'title': 'Справочник рецептов',
            'system_info': 'Дата создания: 25.12.2021 12:00, Контрагент: ООО "", Проведен',
            'receipt': r,
            }
    return django.shortcuts.render(request, 'directory/receipt.html', data)


class ContragentsDetailView(UpdateView):
    # model = Contragents
    model = forms.Contragents
    form_class = forms.ContragentForm
    # fields = ('contragents_id', 'name', 'fullname', 'address', 'phone', 'e_mail', 'note')
    template_name = 'directory/contragents_detail.html'
    context_object_name = 'contragents_detail'

    def get(self, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if (form.is_valid()):
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        return django.shortcuts.HttpResponseRedirect(forms.reverse('contragents'))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class ContragentsCreateView(CreateView):
    model = forms.Contragents
    form_class = forms.ContragentForm
    template_name = 'directory/create_contragents.html'
    context_object_name = 'create_contragents'
    success_url = '/directory/contragents'

    def get(self, request, pk=None, *args, **kwargs):
        if pk == None:
            self.object = None
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            messages.success(request, 'Контрагент создан успешно!')
            return self.render_to_response(
                self.get_context_data(form=form)
            )


class ContragentsDeleteView(DeleteView):
    model = Contragents
    template_name = 'directory/contragents_delete.html'
    success_url = '/directory/contragents'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, 'Контрагент удален успешно!')
        except IntegrityError:
            # result = str(e).rpartition(' ')
            name = self.object
            messages.error(request, 'Контрагент не может быть удален! Существуют записи с этим контрагентом в документах!')
            return render(request, 'directory/contragents_delete.html', context={'name': name.name})
        return HttpResponseRedirect(self.get_success_url())


class MaterialsCreateView(CreateView):
    model = forms.Materials
    form_class = forms.MaterialsForm
    template_name = 'directory/create_materials.html'
    context_object_name = 'create_materials'
    success_url = 'materials'

    def get(self, request, pk=None, *args, **kwargs):
        if pk == None:
            self.object = None
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            return self.render_to_response(
                self.get_context_data(form=form)
            )


class MaterialsDeleteView(DeleteView):
    model = Materials
    template_name = 'directory/materials_delete.html'
    success_url = '/directory/materials'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, 'Материал удален успешно!')
        except IntegrityError:
            # result = str(e).rpartition(' ')
            name = self.object
            messages.error(request, 'Материал не может быть удален! Существуют записи с этим материалом в документах!')
            return render(request, 'directory/materials_delete.html', context={'name': name.name})
        return HttpResponseRedirect(self.get_success_url())


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'directory/category_delete.html'
    success_url = '/directory/category'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, 'Категория удалена успешно!')
        except IntegrityError as e:
            name = self.object
            messages.error(request, 'Категория не может быть удалена! Существуют записи с этой категорией в материалах!')
            return render(request, 'directory/category_delete.html', context={'name': name.name})
        return HttpResponseRedirect(self.get_success_url())


class CoeficientDeleteView(DeleteView):
    model = Coeficient
    template_name = 'directory/coeficient_delete.html'
    success_url = '/directory/coeficient'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, 'Коэффициент удален успешно!')
        except IntegrityError as e:
            name = self.object
            messages.error(request, 'Коэффициент не может быть удален! Существуют записи с этим коэффициентом в документах!')
            return render(request, 'directory/coeficient_delete.html', context={'name': name.name})
        return HttpResponseRedirect(self.get_success_url())


class UnitDeleteView(DeleteView):
    model = Unit
    template_name = 'directory/unit_delete.html'
    success_url = '/directory/unit'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, 'Единица измерения удалена успешно!')
        except IntegrityError as e:
            name = self.object
            messages.error(request, 'Единица измерения не может быть удалена! Существуют записи с этой единицей в документах!')
            return render(request, 'directory/unit_delete.html', context={'name': name.name})
        return HttpResponseRedirect(self.get_success_url())


class ReceptDeleteView(DeleteView):
    model = Receipt
    template_name = 'directory/recept_delete.html'
    success_url = '/directory/receipt'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        recdet = ReceiptDetail.objects.filter(receipt=self.object)
        reg_filter = RegisterReceipt.objects.filter(receipt=self.object)
        reg = RegisterReceipt.objects.get(receipt=self.object)
        reg_comp = RegisterReceiptComposition.objects.filter(register_receipt=reg)
        success_url = self.get_success_url()
        reg_comp.delete()
        if reg_filter.count() <= 1:
            reg_filter.delete()
        else:
            for i in reg_filter:
                i.delete()
        recdet.delete()
        self.object.delete()
        return HttpResponseRedirect(success_url)


class MaterialsDetailView(UpdateView):
    # model = Contragents
    model = forms.Materials
    form_class = forms.MaterialsForm

    template_name = 'directory/materials_detail.html'
    context_object_name = 'materials_detail'

    def get(self, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if (form.is_valid()):
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        return django.shortcuts.HttpResponseRedirect(forms.reverse('materials'))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class CategoryDetailView(UpdateView):
    # model = Contragents
    model = forms.Category
    form_class = forms.CategoryForm

    template_name = 'directory/category_detail.html'
    context_object_name = 'category_detail'

    def get(self, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if (form.is_valid()):
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        return django.shortcuts.HttpResponseRedirect(forms.reverse('category'))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class CategoryCreateView(CreateView):
    model = forms.Category
    form_class = forms.CategoryForm
    template_name = 'directory/create_category.html'
    context_object_name = 'create_category'
    success_url = 'category'

    def get(self, request, pk=None, *args, **kwargs):
        if pk == None:
            self.object = None
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            return self.render_to_response(
                self.get_context_data(form=form)
            )


class UnitCreateView(CreateView):
    model = forms.Unit
    form_class = forms.UnitForm
    template_name = 'directory/create_unit.html'
    context_object_name = 'create_unit'
    success_url = 'unit'

    def get(self, request, pk=None, *args, **kwargs):
        if pk == None:
            self.object = None
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            return self.render_to_response(
                self.get_context_data(form=form)
            )


class UnitDetailView(UpdateView):
    # model = Contragents
    model = forms.Unit
    form_class = forms.UnitForm

    template_name = 'directory/unit_detail.html'
    context_object_name = 'unit_detail'

    def get(self, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if (form.is_valid()):
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        return django.shortcuts.HttpResponseRedirect(forms.reverse('unit'))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class CoeficientDetailView(UpdateView):
    # model = Contragents
    model = forms.Coeficient
    form_class = forms.CoeficientForm

    template_name = 'directory/coeficient_detail.html'
    context_object_name = 'coeficient_detail'

    def get(self, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        return django.shortcuts.HttpResponseRedirect(forms.reverse('coeficient'))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class CoeficientCreateView(CreateView):
    model = forms.Coeficient
    form_class = forms.CoeficientForm
    template_name = 'directory/create_coeficient.html'
    context_object_name = 'create_coeficient'
    success_url = 'coeficient'

    def get(self, request, pk=None, *args, **kwargs):
        if pk == None:
            self.object = None
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            return self.render_to_response(
                self.get_context_data(form=form)
            )


class ReceiptCreateView(CreateView):

    model = forms.Receipt
    form_class = forms.ReceiptForm
    template_name = 'directory/create_receipt.html'
    context_object_name = 'create_receipt'
    success_url = 'receipt'

    def get(self, request, pk=None, *args, **kwargs):

        if not pk:
            self.object = None
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            doc_form = forms.ReceiptDetailFormSet()
            forms.ReceiptFormHelper()
            return self.render_to_response(
                self.get_context_data(form=form, doc_form=doc_form)
            )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        doc_form = forms.ReceiptDetailFormSet(self.request.POST)
        if form.is_valid() and doc_form.is_valid():
            return self.form_valid(form, doc_form)
        return self.form_invalid(form, doc_form)

    def form_valid(self, form, doc_form):
        self.object = form.save()
        doc_form.instance = self.object
        ref = doc_form.save()
        Move.move_receipt(self.object, ref)

        return django.shortcuts.HttpResponseRedirect(forms.reverse('receipt_detail', args=[str(self.object.pk)]))

    def form_invalid(self, form, doc_form):
        return self.render_to_response(self.get_context_data(form=form, doc_form=doc_form))

    def get_context_data(self, **kwargs):
        """ Add formset and formhelper to the context_data. """
        number_last_object = forms.Document.objects.order_by('number').last()
        if not number_last_object:
            number_last = 1
        else:
            number_last = number_last_object.number + 1

        ctx = super(ReceiptCreateView, self).get_context_data(**kwargs)
        doc_formhelper = forms.ReceiptFormHelper()

        if self.request.POST:
            ctx['form'] = forms.ReceiptForm(self.request.POST)
            ctx['doc_form'] = forms.ReceiptDetailFormSet(self.request.POST)
            ctx['doc_formhelper'] = doc_formhelper
        else:
            ctx['form'] = forms.ReceiptForm(initial={'number': number_last})
            ctx['doc_form'] = forms.ReceiptDetailFormSet()
            ctx['doc_formhelper'] = doc_formhelper
        return ctx


class UpdateRecView(UpdateView):
    model = forms.Receipt
    form_class = forms.ReceiptForm
    template_name = 'directory/receipt_detail.html'
    context_object_name = 'receipt_detail'

    def get(self, request, pk=None, *args, **kwargs):
        if pk != None:
            self.object =self.get_object()
            main = Receipt.objects.get(pk=pk)
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            doc_form = forms.RecFormSet(instance=self.object)
            forms.ReceiptFormHelper()
            return self.render_to_response(self.get_context_data(form=form, doc_form=doc_form))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = forms.RecFormSet(self.request.POST, instance=self.object)
        if formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.instance = self.object
        ref = formset.save()
        Move.move_receipt(self.object, ref)
        return django.shortcuts.HttpResponseRedirect(forms.reverse('receipt'))

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))


