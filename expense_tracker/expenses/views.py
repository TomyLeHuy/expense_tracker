# Create your views here.
from django.shortcuts import render, redirect
from .models import Expense
from .forms import ExpenseForm
from collections import defaultdict


from django.shortcuts import render, redirect
from .models import Expense
from .forms import ExpenseForm


def expense_list(request):
    expenses = Expense.objects.all()
    expenses_by_category = {}
    category_sums = {}

    for expense in expenses:
        if expense.category not in expenses_by_category:
            expenses_by_category[expense.category] = []
        expenses_by_category[expense.category].append(expense)

    for category, exp_list in expenses_by_category.items():
        category_sums[category] = sum(exp.amount for exp in exp_list)

    categorized_expenses = [
        {'category': category, 'expenses': expenses, 'total': category_sums[category]}
        for category, expenses in expenses_by_category.items()
    ]

    return render(request, 'expenses/expense_list.html', {
        'categorized_expenses': categorized_expenses
    })



def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/add_expense.html', {'form': form})


def edit_expense(request, pk):
    expense = Expense.objects.get(pk=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expenses/edit_expense.html', {'form': form})


def delete_expense(request, pk):
    expense = Expense.objects.get(pk=pk)
    expense.delete()
    return redirect('expense_list')


def clear_expenses(request):
    if request.method == 'POST':
        Expense.objects.all().delete()
        return redirect('expense_list')
    return render(request, 'expenses/clear_expenses.html')
