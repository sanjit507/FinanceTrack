from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
 
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class TransactionForm(forms.ModelForm):
    class Meta:
        from .models import Transaction
        model = Transaction
        fields = ['title', 'amount', 'date', 'Transaction_type']
class GoalForm(forms.ModelForm):
    class Meta:
        from .models import Goal
        model = Goal
        fields = ['name', 'target_amount', 'current_amount', 'deadline']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'target_amount': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'current_amount': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'deadline': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
        }
        