from django.shortcuts import render, redirect
from fin_bot.forms import SubmitForm, ExpenditureForm, IncomeForm
from fin_bot.models import ExpenditureModel, IncomeModel
from django.contrib import messages
# Create your views here.


def index(request):
    return render(request, 'index.html')


def home(request):
    f = SubmitForm()
    if request.method == 'POST':
        temp = request.POST['type']
        if temp == '1':
            return redirect('home_income')
        else:
            return redirect('home_expenditure')

    return render(request, 'home.html', {'form': f, 'inc': IncomeModel.objects.all()})


def home_income(request):
    income = IncomeForm()
    if request.method == 'POST':
        is_periodical = False
        data = request.POST
        if 'is_periodical' in data:
            is_periodical = True
        inc_model = IncomeModel(
            category=data['category'],
            name=data['name'],
            value=data['value'],
            is_periodical=is_periodical
        )
        inc_model.save()
        messages.success(request, 'Your incomes added successfully')
        return redirect('home')
    return render(request, 'income.html', {'inc_form': income})


def home_expenditure(request):
    exp = ExpenditureForm()
    if request.method == 'POST':
        messages.success(request, 'Your expenditure added successfully')
        return redirect('home')
    return render(request, 'exp_form.html', {'exp_form': exp})

