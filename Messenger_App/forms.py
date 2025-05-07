from django import forms

class AuthorizationForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    email_verification = forms.CharField(label='Email verification')
