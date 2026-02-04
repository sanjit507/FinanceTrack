from django.shortcuts import render
from django.views import View
from finance.form import GoalForm, RegisterForm, TransactionForm
from django.contrib.auth import login
from django.shortcuts import redirect
import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Transaction
from .models import Goal
from django.db import models
import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.contrib import messages


logger = logging.getLogger(__name__)
def home(request):
    return render(request, 'finance/index.html')


class RegisterView(View):
    def get(self, request, *args, **kwargs ):
        form=RegisterForm()
        return render(request, 'finance/reg.html',{'form':form})
    def post(self, request, *args, **kwargs ):
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('dashboard')
        # Log form errors for debugging
        if form.errors:
            logger.debug('Registration form errors: %s', form.errors)
            print('Registration form errors:', form.errors)
        return render(request, 'finance/reg.html',{'form':form})  
    
class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        transactions = Transaction.objects.filter(user=request.user)
        goals = Goal.objects.filter(user=request.user)



        # calculate total income and expenses
        total_income = Transaction.objects.filter(user=request.user, Transaction_type='income').aggregate(models.Sum('amount'))['amount__sum'] or 0
        total_expense = Transaction.objects.filter(user=request.user, Transaction_type='expense').aggregate(models.Sum('amount'))['amount__sum'] or 0
        net_savings = total_income - total_expense
        # remaining_savings starts as net_savings (available to allocate to goals)
        remaining_savings = net_savings
        goal_progress = []
        for goal in goals:
            # compute progress based on available remaining_savings and goal.target_amount
            if remaining_savings >= goal.target_amount:
                progress = 100.0
                remaining_savings -= goal.target_amount
            elif remaining_savings > 0:
                progress = (remaining_savings / goal.target_amount) * 100
                remaining_savings = 0
            else:
                progress = 0.0

            # clamp progress and include current_amount from the model if present
            try:
                current_amount = float(goal.current_amount) if getattr(goal, 'current_amount', None) is not None else 0.0
            except Exception:
                current_amount = 0.0

            progress = max(0.0, min(100.0, float(progress)))
            goal_progress.append({'goal': goal, 'progress': progress, 'current_amount': current_amount})

                 
               

        context = {
            'transactions': transactions,
            'goals': goals,
            'total_income': total_income,
            'total_expense': total_expense,
            'net_savings': net_savings,
            'goal_progress': goal_progress,     
        }
        return render(request, 'finance/dashboard.html', context)


@login_required
def export_transactions(request):
    """Export the current user's transactions as CSV."""
    transactions = Transaction.objects.filter(user=request.user)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transactions.csv"'
    writer = csv.writer(response)
    writer.writerow(['Title', 'Amount', 'Date', 'Type', 'Category'])
    for t in transactions:
        date_val = t.date.isoformat() if getattr(t, 'date', None) else ''
        writer.writerow([t.title, t.amount, date_val, t.Transaction_type, getattr(t, 'category', '')])
    return response  


class GoalListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        goals = Goal.objects.filter(user=request.user)
        return render(request, 'finance/goal_list.html', {'goals': goals})


class GoalUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        goal = get_object_or_404(Goal, pk=pk, user=request.user)
        form = GoalForm(instance=goal)
        return render(request, 'finance/goal_form.html', {'form': form, 'goal': goal, 'is_edit': True})

    def post(self, request, pk, *args, **kwargs):
        goal = get_object_or_404(Goal, pk=pk, user=request.user)
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            g = form.save(commit=False)
            g.user = request.user
            g.save()
            return redirect('goal_list')
        return render(request, 'finance/goal_form.html', {'form': form, 'goal': goal, 'is_edit': True})


class GoalDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        goal = get_object_or_404(Goal, pk=pk, user=request.user)
        return render(request, 'finance/goal_confirm_delete.html', {'goal': goal})

    def post(self, request, pk, *args, **kwargs):
        goal = get_object_or_404(Goal, pk=pk, user=request.user)
        goal.delete()
        return redirect('goal_list')


class TransactionDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
        return render(request, 'finance/transaction_confirm_delete.html', {'transaction': transaction})

    def post(self, request, pk, *args, **kwargs):
        transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
        transaction.delete()
        return redirect('transaction_list')
      
class TransactionView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = TransactionForm()
        return render(request, 'finance/transaction.html', {'form': form}) 
    def post(self, request, *args, **kwargs):
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Transaction added successfully.')
            return redirect('dashboard')  
        return render(request, 'finance/transaction.html', {'form': form})
    
class TransactionListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        transactions = Transaction.objects.filter(user=request.user)
        return render(request, 'finance/transaction_list.html', {'transactions': transactions})
    

class GoalView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = GoalForm()
        return render(request, 'finance/goal.html', {'form': form}) 
    def post(self, request, *args, **kwargs):
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, 'Goal added successfully.')
        return render(request, 'finance/goal.html', {'form': form})   