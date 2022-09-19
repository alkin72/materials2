from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *


router = SimpleRouter()

urlpatterns = [
    path('', views.docs_journal, name='docs_journal'),
    path('application_journal', views.application_journal, name='application_journal'),
    path('<int:pk>', views.DocsDetailView.as_view(), name='docs_detail'), # <int:pk>
    path('<int:pk>/docs_detail_receipt/', views.DocsReceiptDetailView.as_view(), name='docs_detail_receipt'), # <int:pk>
    path('create_detail', views.DocumentCreateView.as_view(), name='create_detail'),
    path('delete_objects', views.delete_objects, name='delete_objects'),
    path('delete_receipt', views.delete_receipt, name='delete_receipt'),
    path('create_detail_receipt', views.DocumentReceiptCreateView.as_view(), name='create_detail_receipt'),
    path('create_detail_receipt_move/<int:pk>', views.DocumentReceiptMoveCreateView.as_view(), name='create_detail_receipt_move'),
    path('<int:pk>/upd_doc/', views.UpdateDocsView.as_view(), name='upd_doc'),
    path('<int:pk>/upd_doc_receipt/', views.UpdateDocsReceiptView.as_view(), name='upd_doc_receipt'),
    path('update/', views.docs_app),
   ]
urlpatterns += router.urls
urlpatterns = format_suffix_patterns(urlpatterns)
