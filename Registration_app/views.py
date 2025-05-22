from django.contrib.auth.views import LogoutView
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render 
from django.views.generic.edit import FormView
from django.contrib.auth import login, authenticate 
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model


from .forms import RegistrationForm, CodeConfirmationForm, AuthorizationForm
from .models import Send_Reg_Code

import secrets
import string


User = get_user_model()



class RegistrationView(FormView):
    template_name = 'Registration_app/registration_authorization.html'
    form_class = RegistrationForm


    def get_context_data(self, **kwargs):
        """Додає дані контексту для шаблону."""
        context = super().get_context_data(**kwargs)
        context['form_name'] = self.form_class.__name__ 
        context['title'] = 'Реєстрація'
        context['subtitle'] = 'Приєднуйся до World IT'
        context['view_type'] = 'registration' 
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
            message_body = f"""
Вітаємо у World IT Messenger! 👋

Будь ласка, використайте наступний код для підтвердження вашої електронної адреси:

{code}

Введіть цей код на сторінці підтвердження, щоб завершити реєстрацію.

Дякуємо за приєднання!
Команда World IT Messenger 🚀
"""
            send_mail(
                subject=subject,
                message=message_body,
                from_email=settings.EMAIL_HOST_USER, 
                recipient_list=[email],
                fail_silently=False 
            )
            messages.success(self.request, 'Код підтвердження відправлено на вашу пошту')
            return redirect('confirm_code')
        except Exception as e:
            print(f"Помилка відправки email: {e}")
            messages.error(self.request, 'Виникла помилка при відправленні коду. Спробуйте пізніше.')
            return self.form_invalid(form)

    def form_invalid(self, form):
        """Рендерить шаблон з невалідною формою та помилками."""
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class CodeConfirmationView(FormView):
    template_name = 'Registration_app/registration_authorization.html'
    form_class = CodeConfirmationForm

    def get_context_data(self, **kwargs):
        """Додає дані контексту для шаблону."""
        context = super().get_context_data(**kwargs)
        context['form_name'] = self.form_class.__name__ 
        context['title'] = 'Підтвердження пошти'
        email_to_confirm = self.request.session.get('registration_email', 'вашу пошту')
        context['subtitle'] = f'Ми надіслали 6-значний код на {email_to_confirm}. Введіть його нижче.'
        context['view_type'] = 'confirmation'
        return context

    def form_valid(self, form):
        """Обробляє валідну форму підтвердження коду."""
        entered_code_list = [
            form.cleaned_data.get('code_1', ''),
            form.cleaned_data.get('code_2', ''),
            form.cleaned_data.get('code_3', ''),
            form.cleaned_data.get('code_4', ''),
            form.cleaned_data.get('code_5', ''),
            form.cleaned_data.get('code_6', ''),
        ]
        entered_code = ''.join(entered_code_list)

        verification_code = self.request.session.get('verification_code')
        registration_email = self.request.session.get('registration_email')
        registration_password = self.request.session.get('registration_password')

        is_code_valid = entered_code == verification_code

        if is_code_valid:

            if registration_email and registration_password:
                try:

                    if User.objects.filter(email=registration_email).exists():
                         messages.error(self.request, 'Користувач з такою поштою вже зареєстрований.')

                         if 'registration_email' in self.request.session: del self.request.session['registration_email']
                         if 'registration_password' in self.request.session: del self.request.session['registration_password']
                         if 'verification_code' in self.request.session: del self.request.session['verification_code']
                         return redirect('registration')

                    user = User.objects.create_user(username=registration_email, email=registration_email, password=registration_password)
                    user.is_active = True 
                    user.save()

                    messages.success(self.request, 'Пошта успішно підтверджена! Тепер ви можете увійти.')

                    if 'registration_email' in self.request.session: del self.request.session['registration_email']
                    if 'registration_password' in self.request.session: del self.request.session['registration_password']
                    if 'verification_code' in self.request.session: del self.request.session['verification_code']


                    return redirect('authorization')

                except Exception as e:
                    print(f"Помилка створення користувача після підтвердження: {e}")
                    messages.error(self.request, 'Виникла помилка при завершенні реєстрації. Спробуйте ще раз або зверніться до підтримки.')
                    return redirect('registration')

            else:
                messages.error(self.request, 'Дані реєстрації відсутні в сесії. Будь ласка, почніть реєстрацію заново.')
                if 'registration_email' in self.request.session: del self.request.session['registration_email']
                if 'registration_password' in self.request.session: del self.request.session['registration_password']
                if 'verification_code' in self.request.session: del self.request.session['verification_code']
                return redirect('registration') 

        else:
            messages.error(self.request, 'Невірний код підтвердження')
            form.add_error(None, 'Невірний код підтвердження') 
            return self.form_invalid(form)

    def form_invalid(self, form):
         """Рендерить шаблон з невалідною формою та помилками."""
         context = self.get_context_data(form=form)
         return self.render_to_response(context)



class AuthorizationView(FormView):
    template_name = 'Registration_app/registration_authorization.html'
    form_class = AuthorizationForm


    def get_context_data(self, **kwargs):
        """Додає дані контексту для шаблону."""
        context = super().get_context_data(**kwargs)
        context['form_name'] = self.form_class.__name__ 
        context['title'] = 'Авторизація'
        context['subtitle'] = 'Ради тебе знову бачити!'
        context['view_type'] = 'authorization'
        return context

    def form_valid(self, form):
        email_or_username = form.cleaned_data['email']
        password = form.cleaned_data['password']

        user = authenticate(request=self.request, username=email_or_username, password=password)

        if user is not None:
            if user.is_active:
                login(self.request, user)
                messages.success(self.request, f'Ласкаво просимо, {user.username}!')
                next_url = self.request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect(settings.LOGIN_REDIRECT_URL) 

            else:
                messages.error(self.request, 'Обліковий запис не активовано.')
                form.add_error(None, 'Обліковий запис не активовано.') 
                return self.form_invalid(form)

        else:
            messages.error(self.request, 'Невірний email або пароль.')
            form.add_error(None, 'Невірні облікові дані.') 

            return self.form_invalid(form)

    def form_invalid(self, form):
        """Рендерить шаблон з невалідною формою та помилками."""
        context = self.get_context_data(form=form)
        return self.render_to_response(context)



class CustomLogoutView(LogoutView):

    next_page = reverse_lazy('authorization') 
