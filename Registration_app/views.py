from django.contrib.auth.views import LogoutView
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.contrib.auth import login
from django.urls import reverse_lazy
from .forms import RegistrationForm, CodeConfirmationForm, AuthorizationForm
from Registration_app.models import Send_Reg_Code
import secrets
import string

class RegistrationView(FormView):
    template_name = 'Registration_app/registration_authorization.html'
    form_class = RegistrationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = self.form_class.__name__
        context['title'] = 'Реєстрація'
        context['subtitle'] = 'Приєднуйся до World IT'
        return context

    def form_valid(self, form):
        password = form.cleaned_data['password']
        confirm_password = form.cleaned_data['confirm_password']
        email = form.cleaned_data['email']

        if password != confirm_password:
            form.add_error('confirm_password', 'Пароли не совпадают')
            return self.form_invalid(form)

        code = ''.join(secrets.choice(string.digits) for _ in range(6))
        self.request.session['registration_email'] = email
        self.request.session['registration_password'] = password
        self.request.session['verification_code'] = code

        Send_Reg_Code.objects.update_or_create(
            email=email,
            defaults={'code': code}
        )

        try:
            subject = '✅ Підтвердіть свою електронну адресу для World IT Messenger!'
            message = f"""
Вітаємо у World IT Messenger! 👋

Будь ласка, використайте наступний код для підтвердження вашої електронної адреси:

{code}

Введіть цей код на сторінці підтвердження, щоб завершити реєстрацію.

Дякуємо за приєднання!
Команда World IT Messenger 🚀
"""
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False
            )
            messages.success(self.request, 'Код підтвердження відправлено на вашу пошту')
            return redirect('confirm_code')
        except Exception as e:
            print(e)
            return self.form_invalid(form)

class CodeConfirmationView(FormView):
    template_name = 'Registration_app/registration_authorization.html'
    form_class = CodeConfirmationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = self.form_class.__name__
        context['title'] = 'Підтвердження пошти'
        context['subtitle'] = f'Ми надіслали 6-значний код на вашу пошту ({self.request.session.get("registration_email")}). Введіть його нижче.'
        return context

    def form_valid(self, form):
        entered_code = ''.join([
            form.cleaned_data.get('code_1', ''),
            form.cleaned_data.get('code_2', ''),
            form.cleaned_data.get('code_3', ''),
            form.cleaned_data.get('code_4', ''),
            form.cleaned_data.get('code_5', ''),
            form.cleaned_data.get('code_6', ''),
        ])

        verification_code = self.request.session.get('verification_code')

        if entered_code == verification_code:
            return redirect('authorization')
        else:
            form.add_error(None, 'Невірний код підтвердження')  
            return self.form_invalid(form)


class AuthorizationView(FormView):
    template_name = 'Registration_app/registration_authorization.html'
    form_class = AuthorizationForm
    success_url = reverse_lazy('messenger')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = self.form_class.__name__
        context['title'] = 'Авторизація'
        context['subtitle'] = 'Ради тебе знову бачити!'
        return context

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        return super().form_valid(form)

class CustomLogoutView(LogoutView):
    next_page = 'authorization'  

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if request.user.is_authenticated:
            request.session['step'] = 'authorization'  
        return response
