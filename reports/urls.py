from django.urls import path
from . import views
from wkhtmltopdf.views import PDFTemplateView
from reports.templates import reports

urlpatterns = [
    path('', views.reports_journal, name='reports_journal'),
    path('expense/', views.expense, name='expense'),
    path('remainder/', views.remainder, name='remainder'),
    path('came/', views.came, name='came'),
    #path('pdf/', views.getpdf, name='pdf'),
    path(r'^came/$', views.PDFView.as_view()),
]
