from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('home/income', views.home_income, name='home_income'),
    path('home/expenditure', views.home_expenditure, name='home_expenditure'),
    path('home/exp_report', views.expenditure_report, name='expenditure_report'),
    path('home/inc_report', views.income_report, name='income_report'),
    path('home/inc/<str:name>/<str:category>/<str:date>', views.income_delete, name='income_delete'),
    path('home/exp/<str:name>/<str:category>/<str:date>', views.exp_delete, name='exp_delete')
]
