from django.shortcuts import render, redirect
from fin_bot.forms import SubmitForm, ExpenditureForm, IncomeForm, ReportForm
from fin_bot.models import ExpenditureModel, IncomeModel
from django.contrib import messages
# Create your views here.


def index(request):
    return render(request, 'index.html')


def home(request):

    f = SubmitForm()
    if request.method == 'POST':
        data_post = request.POST
        if 'add' in data_post.keys():
            if data_post['type'] == '1':
                return redirect('home_income')
            else:
                return redirect('home_expenditure')
        elif 'report' in data_post.keys():
            if data_post['type'] == '1':
                return redirect('income_report')
            else:
                return redirect('expenditure_report')

    return render(request,
                  'home.html',
                  {'form': f, 'inc': IncomeModel.objects.all().order_by('category'),
                   'exp': ExpenditureModel.objects.all().order_by('category')})


def home_income(request):
    income = IncomeForm()
    inc_data = [category['category'] for category in IncomeModel.objects.values('category').distinct()]

    if 'list category' in request.POST.keys():
        income = IncomeForm(initial={'category': request.POST['list category']})
        return render(request, 'income.html', {'inc_form': income, 'inc_data': inc_data})
    if request.method == 'POST':
        is_periodical = False
        data = request.POST
        if 'is_periodical' in data:
            is_periodical = True
        inc_model = IncomeModel(
            category=data['category'],
            name=data['name'],
            value=data['value'],
            date_added=get_date_added(data, 'added'),
            is_periodical=is_periodical
        )
        inc_model.save()
        messages.success(request, 'Your incomes added successfully')
        return redirect('home')
    return render(request, 'income.html', {'inc_form': income, 'inc_data': inc_data})


def home_expenditure(request):
    exp = ExpenditureForm()
    exp_data = [category['category'] for category in ExpenditureModel.objects.values('category').distinct()]

    if 'list category' in request.POST.keys():
        exp = ExpenditureForm(initial={'category': request.POST['list category']})
        return render(request, 'exp_form.html', {'exp_form': exp, 'exp_data': exp_data})
    if request.method == 'POST':
        data = request.POST

        exp_data = ExpenditureModel(
            category=data['category'],
            name=data['name'],
            value=data['value'],
            date_added=get_date_added(data, 'added')
        )
        exp_data.save()
        messages.success(request, 'Your expenditure added successfully')
        return redirect('home')
    return render(request, 'exp_form.html', {'exp_form': exp, 'exp_data': exp_data})


def expenditure_report(request):
    exp_data = ExpenditureModel.objects.all()
    value_sum = sum([val['value'] for val in ExpenditureModel.objects.values('value')])
    categories = [val['category'] for val in ExpenditureModel.objects.values('category').distinct()]

    request_data = request.GET
    if 'filter' in request_data.keys():
        if request_data['filter'] == 'Date':
            new_data = ExpenditureModel.objects.order_by('date_added')
            return render(request, 'exp_report.html',
                          {'exp_data': new_data, 'sum': value_sum, 'date_form': ReportForm(), 'category': categories})
        new_data = ExpenditureModel.objects.order_by(request_data['filter'].lower())
        return render(request, 'exp_report.html', {'exp_data': new_data, 'sum': value_sum, 'date_form': ReportForm(), 'category': categories})

    if 'period' in request_data.keys():
        date_from = get_date_added(request_data, 'from')
        date_to = get_date_added(request_data, 'to')
        exp_data = ExpenditureModel.objects.filter(date_added__gte=date_from, date_added__lte=date_to)
        value_sum = sum([val['value'] for val in exp_data.values('value')])

    if 'rep_cat' in request_data.keys() and request_data['rep_cat'] != 'All':
        exp_data = ExpenditureModel.objects.filter(category=request_data['rep_cat'])
        value_sum = sum([val['value'] for val in exp_data.values('value')])

    return render(request,
                  'exp_report.html',
                  {'exp_data': exp_data, 'sum': value_sum, 'date_form': ReportForm(), 'category': categories})


def income_report(request):
    inc_data = IncomeModel.objects.all()
    categories = [val['category'] for val in IncomeModel.objects.values('category').distinct()]
    value = sum([val['value'] for val in IncomeModel.objects.values('value')])

    request_data = request.GET
    if 'filter' in request_data.keys():
        if request_data['filter'] == 'Date':
            new_data = IncomeModel.objects.order_by('date_added')
            return render(request, 'income_report.html',
                          {'f': new_data, 'sum': value, 'date_form': ReportForm(), 'category': categories})
        new_data = IncomeModel.objects.order_by(request_data['filter'].lower())
        return render(request, 'income_report.html', {'f': new_data, 'sum': value, 'date_form': ReportForm(), 'category': categories})

    if 'period' in request_data.keys():
        date_from = get_date_added(request_data, 'from')
        date_to = get_date_added(request_data, 'to')
        inc_data = IncomeModel.objects.filter(date_added__gte=date_from, date_added__lte=date_to)
        value = sum([val['value'] for val in inc_data.values('value')])

    if 'rep_cat' in request_data.keys() and request_data['rep_cat'] != 'All':
        inc_data = IncomeModel.objects.filter(category=request_data['rep_cat'])
        value = sum([val['value'] for val in inc_data.values('value')])

    return render(request, 'income_report.html',
                  {'f': inc_data, 'sum': value, 'date_form': ReportForm(),
                   'category': categories})


def income_delete(request, category, name, date):
    note = IncomeModel.objects.filter(category=category, name=name, date_added=format_date(date))
    note.delete()
    return redirect('home')


def exp_delete(request, name, category, date):
    note = ExpenditureModel.objects.filter(name=name, category=category, date_added=format_date(date))
    note.delete()
    return redirect('home')


def format_date(date):
    f_date = date.split('-')[:2] + [date.split('-')[2][:2]]
    return '-'.join(f_date)


def get_date_added(data, prefix):
    date = ''
    for item in ['year', 'month', 'day']:
        date += data[f'date_{prefix}_{item}'] + '-'

    return date[:-1]
