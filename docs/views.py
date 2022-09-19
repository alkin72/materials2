import django.shortcuts
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
# from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .utils import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# test ========================================
# class APIDetail(APIView):
#
#     permission_classes = [IsAuthenticated]
#
#     def get(self, reguest):
#         return Response({'key': 'Dmitry247571'})
# test ========================================


# детализация документа===================================
class DocsDetailView(DetailView):
    model = forms.Document
    template_name = 'docs/docs_detail.html'
    context_object_name = 'docs_detail'

    # permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, pk=None):
        docs = forms.Document.objects.all()
        data = {'title': 'Журнал документов',
                'system_info': 'Дата создания: 25.12.2021 12:00, Контрагент: ООО "", Проведен',
                'docs': docs,
                }
        if request.method == 'POST':
            pk = self.kwargs['pk']

            if 'move' in request.POST:
                # проводка документа --------------------
                Move.move_document(pk, 0)
                # конец проводки-------------------------

                return django.shortcuts.render(request, 'docs/docs_journal.html', data)

            elif 'edit' in request.POST:

                return django.shortcuts.render(request, 'docs/update_detail.html')
# детализация документа=================================


# детализация документа рецепта=========================
class DocsReceiptDetailView(DetailView):
    model = forms.DocumentReceipt
    template_name = 'docs/docs_detail_receipt.html'
    context_object_name = 'docs_detail_receipt'

    # permission_classes = [IsAuthenticated, IsAdminUser]
    def get_context_data(self, **kwargs):
        doc_rec = forms.DocumentReceipt.objects.get(doc_receipt_id=self.kwargs['pk'])

        ctx = super().get_context_data(**kwargs)
        if doc_rec.move:
            rel = RelationDoc.objects.get(doc_receipt=self.kwargs['pk'])
            doc = Document.objects.get(doc_id=rel.doc_id)
            mess = 'По документу №' + str(doc_rec.number) + ' существует документ списания №' + str(doc.number) + ' Для отмены нажмите Отмену расчета для ' \
                                                                                                                  'перехода к документу №' + str(doc.number)
            ctx['message'] = mess
        elif RelationDoc.objects.filter(doc_receipt=self.kwargs['pk']) and not doc_rec.move:
            rel = RelationDoc.objects.get(doc_receipt=self.kwargs['pk'])
            doc = Document.objects.get(doc_id=rel.doc_id)
            message_rel = 'По документу №' + str(doc_rec.number) + ' существует документ списания №' + str(doc.number) + ' нельзя создавать повторный ' \
                                                                                                                         'документ, необходимо сначало ' \
                                                                                                                           'удалить предыдущий'
            ctx['message_rel'] = message_rel
            ctx['booling'] = False
        else:
            ctx['booling'] = True
        return ctx

    def post(self, request, pk=None):
        doc_rel = RelationDoc.objects.get(doc_receipt=self.kwargs['pk'])
        data = {'doc': doc_rel}
        ref = DocumentRef.objects.filter(doc_id=doc_rel.doc_id)
        doc = Document.objects.filter(doc_id=doc_rel.doc_id)
        if request.method == 'POST':
            pk = self.kwargs['pk']
            if 'un_move' in request.POST:
                # отмена проводки документа расчета рецепта --------------------
                Move.un_move(pk)
                # отмена проводки документа расчета рецепта -------------------------
                Move.move_document(doc_rel.doc_id, 1)  # проводка или отмена
                doc_rel.delete()  # удаление зависимости документ -> документ рецепт
                ref.delete()  # удаление списка по документу
                doc.delete()  # удаление документа

                return django.shortcuts.HttpResponseRedirect(forms.reverse('docs_detail_receipt', args=(pk,)))
                #return django.shortcuts.render(request, 'docs/application_journal.html', data)
            # elif 'edit' in request.POST:
            #     return django.shortcuts.render(request, 'docs/application_journal.html', data)
            else:
                return django.shortcuts.render(request, 'docs/application_journal.html', data)

# детализация документа рецепта ===================================

# не используем пока ==============================================
# class DocUpdateSerializerView(generics.RetrieveUpdateDestroyAPIView):
#     #queryset = Document.objects.prefetch_related('docs_set')
#     queryset = Document.objects.all()
#     serializer_class = DocumentSerializer
#     permission_class = permissions.IsAuthenticated
#
#
# class DocUpdateSerView(ModelViewSet):
#     queryset = Document.objects.all()
#     serializer_class = DocumentSerializer
#
#
#     def list(self, request):
#         queryset = Document.objects.all()
#         serializer = DocumentSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk=None):
#         queryset = Document.objects.all()
#         doc_ref = get_object_or_404(queryset, pk=pk)
#         serializer = DocumentSerializer(doc_ref)
#         return Response(serializer.data)
# не используем пока ===============================================

# проверка API===============================================================


def docs_app(request):
    return django.shortcuts.render(request, 'docs/update.html')
# проверка API===============================================================
# пока не используем REST framework сериалайзеры ================================


# class DocUpdateView(generics.RetrieveUpdateDestroyAPIView):
#     template_name = 'docs/update_detail.html'
#     renderer_classes = (TemplateHTMLRenderer,)
#     style = {'template_pack': 'rest_framework/vertical/'}
#
#     def get(self, request, pk):
#         doc = get_object_or_404(Document, pk=pk)
#         serializer = DocumentSerializer(doc)
#         return Response({'serializer': serializer, 'doc': doc, 'style': self.style, })
# пока не используем REST framework сериалайзеры  ==============================


# редактирование документа ==================================
class UpdateDocsView(UpdateView):
    model = forms.Document
    form_class = forms.DocumentForm
    template_name = 'docs/upd_doc.html'
    context_object_name = 'upd_doc'

    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            self.object = self.get_object()
            main = Document.objects.get(pk=pk)
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            doc_form = forms.DocFormSet(instance=main)
            forms.DocFormHelper()
            return self.render_to_response(self.get_context_data(form=form, doc_form=doc_form))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = forms.DocFormSet(self.request.POST, instance=self.object)
        # ===
        # form.save()
        # formset.save()
        # return django.shortcuts.HttpResponseRedirect(forms.reverse('docs_detail', args=[str(self.object.pk)]))
        # ===
        if formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        return django.shortcuts.HttpResponseRedirect(forms.reverse('docs_detail', args=[str(self.object.pk)]))

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))
# конец редактирования документа ============================


# редактирование заявки ==================================
class UpdateDocsReceiptView(UpdateView):
    model = forms.DocumentReceipt
    form_class = forms.DocumentReceptForm
    template_name = 'docs/upd_doc_receipt.html'
    context_object_name = 'upd_doc_receipt'

    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            self.object = self.get_object()
            main = DocumentReceipt.objects.get(pk=pk)
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            doc_form = forms.DocReceiptFormSet(instance=main)
            forms.DocFormHelper()
            return self.render_to_response(self.get_context_data(form=form, doc_form=doc_form))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = forms.DocReceiptFormSet(self.request.POST, instance=self.object)

        if formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        return django.shortcuts.HttpResponseRedirect(forms.reverse('docs_detail_receipt', args=[str(self.object.pk)]))

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))
# конец редактирования заявки ============================


# создание документа================================
class DocumentCreateView(CreateView):

    model = forms.Document
    form_class = forms.DocumentForm
    template_name = 'docs/create_detail.html'
    context_object_name = 'create_detail'

    @method_decorator(login_required)
    def get(self, request, pk=None, *args, **kwargs):
        if pk == None:
            self.object = None
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            doc_form = forms.DocumentDetailFormSet()
            forms.DocFormHelper()
            return self.render_to_response(
                self.get_context_data(form=form, doc_form=doc_form)
            )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        doc_form = forms.DocumentDetailFormSet(self.request.POST)
        if form.is_valid() and doc_form.is_valid():
            return self.form_valid(form, doc_form)
        return self.form_invalid(form, doc_form)

    def form_valid(self, form, doc_form):
        self.object = form.save()
        doc_form.instance = self.object
        doc_form.save()
        if self.object.move:
            Document.objects.filter(pk=self.object.pk).update(move=False)
            Move.move_document(self.object.pk, 0)
        return django.shortcuts.HttpResponseRedirect(forms.reverse('docs_detail', args=[str(self.object.pk)]))

    def form_invalid(self, form, doc_form):
        return self.render_to_response(self.get_context_data(form=form, doc_form=doc_form))

    def get_context_data(self, **kwargs):
        """ Add formset and formhelper to the context_data. """
        number_last_object = forms.Document.objects.order_by('number').last()
        number_last = number_last_object.number + 1
        value = 1
        ctx = super(DocumentCreateView, self).get_context_data(**kwargs)
        doc_formhelper = forms.DocFormHelper()

        if self.request.POST:
            ctx['form'] = forms.DocumentForm(self.request.POST)
            ctx['doc_form'] = forms.DocumentDetailFormSet(self.request.POST)
            ctx['doc_formhelper'] = doc_formhelper
        else:
            ctx['form'] = forms.DocumentForm(initial={'number': number_last})

            ctx['doc_form'] = forms.DocumentDetailFormSet()  # initial=[{'materials': 1, 'value': 1, 'unit': 1}, {'materials': 1, 'value': 1,
            # 'unit': 1}]
            ctx['doc_formhelper'] = doc_formhelper
        return ctx
# конец создание документа==============================================


# создание документа списания по рецепту================================
class DocumentReceiptMoveCreateView(CreateView):
    model = forms.Document
    form_class = forms.DocumentForm
    template_name = 'docs/create_detail_receipt_move.html'
    context_object_name = 'create_detail_receipt_move'

    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            self.object = None
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            doc_form = forms.DocumentDetailFormSet()
            forms.DocFormHelper()
            return self.render_to_response(
                self.get_context_data(form=form, doc_form=doc_form)
            )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        doc_form = forms.DocumentDetailFormSet(self.request.POST)
        if form.is_valid() and doc_form.is_valid():
            return self.form_valid(form, doc_form)
        return self.form_invalid(form, doc_form)

    def form_valid(self, form, doc_form):
        doc_receipt = DocumentReceipt.objects.get(doc_receipt_id=self.kwargs.get('pk'))
        # rel = RelationDoc.objects.all()
        self.object = form.save()
        doc_form.instance = self.object
        doc_form.save()
        doc = Document.objects.get(pk=self.object.pk)
        Document.objects.filter(pk=self.object.pk).update(move=False)
        DocumentReceipt.objects.filter(doc_receipt_id=self.kwargs.get('pk')).update(move=True)
        Move.move_document(self.object.pk, 1)
        RelationDoc.objects.create(doc=doc, doc_receipt=doc_receipt)
        return django.shortcuts.HttpResponseRedirect(forms.reverse('docs_detail', args=[str(self.object.pk)]))

    def form_invalid(self, form, doc_form):
        return self.render_to_response(self.get_context_data(form=form, doc_form=doc_form))

    def get_context_data(self, **kwargs):
        """ Add formset and formhelper to the context_data. """
        pk = self.kwargs.get('pk')
        number_last_object = forms.Document.objects.order_by('number').last()
        number_last = number_last_object.number + 1
        data_form = DocumentReceipt.objects.get(pk=pk)
        data_formset = Move.move_receipt(pk, data_form.datetime)
        note = "расход по заявке №" + str(data_form.number) + " от " + str(data_form.datetime)
        ctx = super(DocumentReceiptMoveCreateView, self).get_context_data(**kwargs)
        doc_formhelper = forms.DocFormHelper()

        if self.request.POST:
            ctx['form'] = forms.DocumentForm(self.request.POST)
            ctx['doc_form'] = forms.DocumentDetailFormSet(self.request.POST)
            ctx['doc_formhelper'] = doc_formhelper
        else:
            ctx['form'] = forms.DocumentForm(initial={'number': number_last, 'datetime': data_form.datetime, 'category_move': False,
                                             'holding': data_form.holding,
                                                      'contragent': data_form.contragent_id, 'note': note})
            ctx['doc_form'] = forms.DocumentDetailFormSet(initial=data_formset)
            ctx['doc_formhelper'] = doc_formhelper
        return ctx
# конец создание документа списания по рецепту=======================================================


# создание документа заявки ================================
class DocumentReceiptCreateView(CreateView):
    model = forms.DocumentReceipt
    form_class = forms.DocumentReceptForm
    template_name = 'docs/create_detail_receipt.html'
    context_object_name = 'create_detail_receipt'

    @method_decorator(login_required)
    def get(self, request, pk=None, *args, **kwargs):
        if pk == None:
            self.object = None
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            doc_form = forms.DocumentReceiptDetailFormSet()
            forms.DocReceiptFormHelper()
            return self.render_to_response(
                self.get_context_data(form=form, doc_form=doc_form)
            )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        doc_form = forms.DocumentReceiptDetailFormSet(self.request.POST)
        if form.is_valid() and doc_form.is_valid():
            return self.form_valid(form, doc_form)
        return self.form_invalid(form, doc_form)

    def form_valid(self, form, doc_form):
        self.object = form.save()
        doc_form.instance = self.object
        doc_form.save()
        # if self.object.move:
        #     DocumentReceipt.objects.filter(pk=self.object.pk).update(move=False)
            #Move.move_document(self.object.pk)
        return django.shortcuts.HttpResponseRedirect(forms.reverse('docs_detail_receipt', args=[str(self.object.pk)]))

    def form_invalid(self, form, doc_form):
        return self.render_to_response(self.get_context_data(form=form, doc_form=doc_form))

    def get_context_data(self, **kwargs):
        """ Add formset and formhelper to the context_data. """
        number_last_object = forms.DocumentReceipt.objects.order_by('number').last()

        if number_last_object:
            number_last = number_last_object.number + 1
        else:
            number_last = 1
        ctx = super(DocumentReceiptCreateView, self).get_context_data(**kwargs)
        doc_formhelper = forms.DocReceiptFormHelper()

        if self.request.POST:
            ctx['form'] = forms.DocumentReceptForm(self.request.POST)
            ctx['doc_form'] = forms.DocumentReceiptDetailFormSet(self.request.POST)
            ctx['doc_formhelper'] = doc_formhelper
        else:
            ctx['form'] = forms.DocumentReceptForm(initial={'number': number_last})
            ctx['doc_form'] = forms.DocumentReceiptDetailFormSet()
            ctx['doc_formhelper'] = doc_formhelper
        return ctx
# конец создание документа заявки=======================================================


# журнал документов==============================================================
@login_required()
def docs_journal(request):
    docs = forms.Document.objects.all()

    data = {'title': 'Журнал документов',
            'system_info': 'Дата создания: 25.12.2021 12:00, Контрагент: ООО "", Проведен',
            'docs': docs,
            }

    return django.shortcuts.render(request, 'docs/docs_journal.html', data)
# конец журнал документов ======================================================


# журнал заявок==============================================================
@ login_required()
def application_journal(request):
    docs = forms.DocumentReceipt.objects.all()

    data = {'title': 'Журнал заявок',
            'system_info': 'Дата создания: 25.12.2021 12:00, Контрагент: ООО "", Проведен',
            'docs': docs,
            }
    return django.shortcuts.render(request, 'docs/application_journal.html', data)
# конец журнал заявок ======================================================


# удаление помеченных объектов==============================================
@ login_required()
def delete_objects(request):
    delete_docs = forms.Document.objects.filter(isdelete=True)
    docs = forms.Document.objects.all()
    docs_ref = DocumentRef.objects.filter(doc__in=delete_docs)
    data = {'delete_object': delete_docs, 'docs': docs}
    #docs.delete()
    if request.method == 'POST':
        if 'delete' in request.POST:
            docs_ref.delete()
            delete_docs.delete()
            return django.shortcuts.render(request, 'docs/docs_journal.html', data)
        elif 'cancel' in request.POST:
            return django.shortcuts.render(request, 'docs/docs_journal.html', data)
    return django.shortcuts.render(request, 'docs/delete_objects.html', data)
# удаление помеченных объектов==============================================


# удаление помеченных объектов==============================================
@ login_required()
def delete_receipt(request):
    list_rec = []
    delete_docs = forms.DocumentReceipt.objects.filter(isdelete=True)
    docs = forms.DocumentReceipt.objects.all()
    docs_ref = DocumentReceiptRef.objects.filter(doc_receipt__in=delete_docs)
    rel = RelationDoc.objects.filter(doc_receipt__in=delete_docs)
    for i in docs_ref:
        list_rec.append(i.receipt_id)
    receipt = Receipt.objects.filter(receipt_id__in=list_rec)
    reg_rec = RegisterReceipt.objects.filter(receipt__in=receipt)
    reg_rec_comp = RegisterReceiptComposition.objects.filter(register_receipt__in=reg_rec)
    data = {'delete_object': delete_docs, 'docs_ref': docs_ref, 'docs': docs}

    if request.method == 'POST':
        if 'delete' in request.POST:
            # reg_rec_comp.delete()
            # reg_rec.delete()
            rel.delete()
            docs_ref.delete()
            delete_docs.delete()
            return django.shortcuts.render(request, 'docs/application_journal.html', data)
        elif 'cancel' in request.POST:
            return django.shortcuts.render(request, 'docs/application_journal.html', data)
    return django.shortcuts.render(request, 'docs/delete_receipt.html', data)
# удаление помеченных объектов==============================================
