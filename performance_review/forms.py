from django import forms
from django.forms import PasswordInput, EmailInput

from .models import *
from django.contrib.auth.models import User


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = (
            'profile_image', 'gender', 'contact_no', 'address', 'address', 'nic', 'org_id', 'rank', 'date_of_birth', 'joined_on',
        )


class UserRegisterForm(forms.ModelForm):

    password = forms.CharField(
        widget=PasswordInput,
        help_text='Password must have more then 8 chars, Letters, Symbols and Numbers must be used'
    )
    email = forms.CharField(widget=EmailInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', "password", 'is_active')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_active')

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'
