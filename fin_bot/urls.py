from django.urls import path
from fin_bot.views import index, home, home_income, home_expenditure

urlpatterns = [
    path('', index, name='index'),
    path('home/', home, name='home'),
    path('home/income', home_income, name='home_income'),
    path('home/expenditure', home_expenditure, name='home_expenditure')
]
