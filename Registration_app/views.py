from django.shortcuts import render
from django.views.generic.edit import FormView
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import RegistrationForm
from .models import Send_Reg_Code
import secrets
import string

class render_registration_page(FormView):
    template_name = 'Registration_app/registration.html'
    form_class = RegistrationForm
    success_url = '/authorization'

    def form_valid(self, form):
        password = form.cleaned_data['password']
        confirm_password = form.cleaned_data['confirm_password']
        email = form.cleaned_data['email']

        if password != confirm_password:
            form.add_error('confirm_password', 'Пароли не совпадают')
            return self.form_invalid(form)

        code = ''.join(secrets.choice(string.digits) for _ in range(6))

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

        except Exception as e:
            print(e)

        return super().form_valid(form)