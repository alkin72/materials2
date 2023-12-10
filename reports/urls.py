from django.urls import path
from . import views
from reports.templates import reports


urlpatterns = [
    path('', views.reports_journal, name='reports_journal'),
    path('expense/', views.expense, name='expense'),
    path('remainder/', views.remainder, name='remainder'),
    path('came/', views.came, name='came'),
    path('pdf/', views.generate_pdf, name='pdf'),
    path('receipt_data/', views.receipt_data, name='receipt_data'),
]