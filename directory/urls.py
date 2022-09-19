from django.urls import path
from requests import request
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.directory, name='directory'),
    path('create_contragents', views.ContragentsCreateView.as_view(), name='create_contragents'),
    path('contragents/', views.contragents, name='contragents'),
    path('materials/', views.materials, name='materials'),
    path('category/', views.category, name='category'),
    path('unit/', views.unit, name='unit'),
    path('coeficient/', views.coeficient, name='coeficient'),
    path('receipt/', views.receipt, name='receipt'),
    path('category-materials/<int:pk>', views.CategoryDetailView.as_view(), name='category_detail'),
    path('category-materials/<int:pk>/delete', views.CategoryDeleteView.as_view(), name='category_delete'),
    path('coeficient/<int:pk>', views.CoeficientDetailView.as_view(), name='coeficient_detail'),
    path('coeficient/<int:pk>/delete', views.CoeficientDeleteView.as_view(), name='coeficient_delete'),
    path('unit/<int:pk>', views.UnitDetailView.as_view(), name='unit_detail'),
    path('unit/<int:pk>/delete', views.UnitDeleteView.as_view(), name='unit_delete'),
    path('create_category', views.CategoryCreateView.as_view(), name='create_category'),
    path('create_unit', views.UnitCreateView.as_view(), name='create_unit'),
    path('create_coeficient', views.CoeficientCreateView.as_view(), name='create_coeficient'),
    path('create_materials', views.MaterialsCreateView.as_view(), name='create_materials'),
    path('create_receipt', views.ReceiptCreateView.as_view(), name='create_receipt'),
    path('contragents/<int:pk>', views.ContragentsDetailView.as_view(), name='contragents_detail'),
    path('contragents/<int:pk>/delete', views.ContragentsDeleteView.as_view(), name='contragents_delete'),
    path('materials/<int:pk>', views.MaterialsDetailView.as_view(), name='materials_detail'),
    path('materials/<int:pk>/delete', views.MaterialsDeleteView.as_view(), name='materials_delete'),
    path('receipt/<int:pk>', views.UpdateRecView.as_view(), name='receipt_detail'),
    path('receipt/<int:pk>/delete', views.ReceptDeleteView.as_view(), name='receipt_delete'),
]
urlpatterns = format_suffix_patterns(urlpatterns)