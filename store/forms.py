from django import forms
from .models import Customer, Dealer, Employee, Medicine, Purchase


class EmployeeForm(forms.ModelForm):
    model = Employee
    fields = "__all__"
