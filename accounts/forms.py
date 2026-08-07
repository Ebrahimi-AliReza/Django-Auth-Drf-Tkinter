from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class loginForm(forms.Form):
    email = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    


class registerForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields =('email','password1', 'password2')

class changepasswordForm(forms.Form):
    current_password = forms.CharField(max_length=20)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(required=True)
    
class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)