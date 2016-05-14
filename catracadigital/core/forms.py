from django import forms
from .models import Employee


class LoginForm(forms.Form):
    username = forms.CharField(label='Nome do usuário', max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'mobile_id', 'company']