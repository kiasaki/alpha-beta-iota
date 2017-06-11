from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from app.models import Account


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AccountForm(forms.ModelForm):
    name = forms.CharField(label='Account Name', max_length=254)

    class Meta:
        model = Account
        fields = ['name']
