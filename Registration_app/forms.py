from django import forms

class RegistrationForm(forms.Form):
    email = forms.EmailField(
        label='Електронна пошта',
        widget=forms.EmailInput(attrs={
            'placeholder': 'you@example.com',
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Введи пароль',
            'class': 'form-control'
        })
    )
    confirm_password = forms.CharField(
        label='Підтверди пароль',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Повтори пароль',
            'class': 'form-control'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Паролі не співпадають.")
        return cleaned_data

class CodeConfirmationForm(forms.Form):
    code_1 = forms.CharField(
        max_length=1,
        widget=forms.TextInput(attrs={
            'class': 'code-input',
            'placeholder': '___',
            'autocomplete': 'off',
        })
    )
    code_2 = forms.CharField(
        max_length=1,
        widget=forms.TextInput(attrs={
            'class': 'code-input',
            'placeholder': '___',
            'autocomplete': 'off',
        })
    )
    code_3 = forms.CharField(
        max_length=1,
        widget=forms.TextInput(attrs={
            'class': 'code-input',
            'placeholder': '___',
            'autocomplete': 'off',
        })
    )
    code_4 = forms.CharField(
        max_length=1,
        widget=forms.TextInput(attrs={
            'class': 'code-input',
            'placeholder': '___',
            'autocomplete': 'off',
        })
    )
    code_5 = forms.CharField(
        max_length=1,
        widget=forms.TextInput(attrs={
            'class': 'code-input',
            'placeholder': '___',
            'autocomplete': 'off',
        })
    )
    code_6 = forms.CharField(
        max_length=1,
        widget=forms.TextInput(attrs={
            'class': 'code-input',
            'placeholder': '___',
            'autocomplete': 'off',
        })
    )

class AuthorizationForm(forms.Form):
    email = forms.EmailField(
        label='Електронна пошта',
        widget=forms.EmailInput(attrs={
            'placeholder': 'you@example.com',
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Введи пароль',
            'class': 'form-control'
        })
    )