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
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

class RegistrationView(FormView):
    template_name = 'Registration_app/registration_authorization.html'
    form_class = RegistrationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = self.form_class.__name__
        context['title'] = 'Реєстрація'
        context['subtitle'] = 'Приєднуйся до World IT'
        context['view_type'] = 'registration'
        return context

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        code = ''.join(secrets.choice(string.digits) for _ in range(6))

        self.request.session['registration_email'] = email
        self.request.session['registration_password'] = password
        self.request.session['verification_code'] = code

        Send_Reg_Code.objects.update_or_create(
            email=email,
            defaults={
                'code': code,
                'expires_at': timezone.now() + timezone.timedelta(minutes=15)
            }
        )

        try:
            subject = '✅ Підтвердіть свою електронну адресу для World IT Messenger!'
            message_body = f"""
Вітаємо у World IT Messenger! 👋

Будь ласка, використайте наступний код для підтвердження вашої електронної адреси:

{code}

Введіть цей код на сторінці підтвердження, щоб завершити реєстрацію. Код дійсний 15 хвилин.

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
            messages.success(self.request, 'Код підтвердження відправлено на вашу пошту.')
            logger.info(f"Verification code sent to {email}")
            return redirect('confirm_code')
        except Exception as e:
            logger.error(f"Error sending email to {email}: {e}")
            messages.error(self.request, 'Виникла помилка при відправленні коду. Спробуйте ще раз або зверніться до підтримки.')
            self._cleanup_session()
            return self.form_invalid(form)

    def form_invalid(self, form):
        logger.warning(f"Invalid registration form: {form.errors}")
        self._cleanup_session()
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def _cleanup_session(self):
        """Helper method to clean up session data."""
        session_keys = ['registration_email', 'registration_password', 'verification_code']
        for key in session_keys:
            self.request.session.pop(key, None)

class CodeConfirmationView(FormView):
    template_name = 'Registration_app/registration_authorization.html'
    form_class = CodeConfirmationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = self.form_class.__name__
        context['title'] = 'Підтвердження пошти'
        email = self.request.session.get('registration_email', 'вашу пошту')
        context['subtitle'] = f'Ми надіслали 6-значний код на {email}. Введіть його нижче.'
        context['view_type'] = 'confirmation'
        return context

    def form_valid(self, form):
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
        try:
            reg_code = Send_Reg_Code.objects.get(email=registration_email)
            is_code_valid = entered_code == verification_code == reg_code.code
            is_code_not_expired = reg_code.expires_at > timezone.now()
        except Send_Reg_Code.DoesNotExist:
            is_code_valid = False
            is_code_not_expired = False

        if is_code_valid and is_code_not_expired:
            if registration_email and registration_password:
                try:
                    if User.objects.filter(email=registration_email).exists():
                        messages.error(self.request, 'Користувач з такою поштою вже зареєстрований.')
                        logger.warning(f"Duplicate email attempted: {registration_email}")
                        self._cleanup_session()
                        Send_Reg_Code.objects.filter(email=registration_email).delete()
                        return redirect('registration')

                    user = User.objects.create_user(
                        username=registration_email,
                        email=registration_email,
                        password=registration_password
                    )
                    user.is_active = True
                    user.save()

                    messages.success(self.request, 'Реєстрація завершена. Тепер ви можете увійти.')
                    self._cleanup_session()
                    Send_Reg_Code.objects.filter(email=registration_email).delete()
                    logger.info(f"User {registration_email} registered successfully")
                    return redirect('authorization')

                except Exception as e:
                    logger.error(f"Error creating user {registration_email}: {e}")
                    messages.error(self.request, 'Виникла помилка при завершенні реєстрації. Спробуйте ще раз або зверніться до підтримки.')
                    self._cleanup_session()
                    return redirect('registration')
            else:
                messages.error(self.request, 'Дані реєстрації відсутні в сесії. Почніть реєстрацію заново.')
                logger.warning("Missing session data during code confirmation")
                self._cleanup_session()
                return redirect('registration')
        else:
            messages.error(self.request, 'Невірний або прострочений код підтвердження.')
            form.add_error(None, 'Невірний або прострочений код підтвердження.')
            logger.warning(f"Invalid or expired code for {registration_email}: {entered_code}")
            return self.form_invalid(form)

    def post(self, request, *args, **kwargs):
        if 'resend_code' in request.POST:
            email = request.session.get('registration_email')
            if email:
                code = ''.join(secrets.choice(string.digits) for _ in range(6))
                request.session['verification_code'] = code
                Send_Reg_Code.objects.update_or_create(
                    email=email,
                    defaults={
                        'code': code,
                        'expires_at': timezone.now() + timezone.timedelta(minutes=15)
                    }
                )
                try:
                    send_mail(
                        subject='✅ Новий код підтвердження для World IT Messenger!',
                        message=f"Ваш новий код підтвердження: {code}\nКод дійсний 15 хвилин.",
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[email],
                        fail_silently=False
                    )
                    messages.success(request, 'Новий код надіслано на вашу пошту.')
                    logger.info(f"Resent verification code to {email}")
                except Exception as e:
                    logger.error(f"Error resending email to {email}: {e}")
                    messages.error(request, 'Не вдалося надіслати новий код. Спробуйте пізніше.')
                    self._cleanup_session()
            else:
                messages.error(request, 'Дані реєстрації відсутні. Почніть заново.')
                self._cleanup_session()
                return redirect('registration')
            return redirect('confirm_code')
        return super().post(request, *args, **kwargs)

    def _cleanup_session(self):
        """Helper method to clean up session data."""
        session_keys = ['registration_email', 'registration_password', 'verification_code']
        for key in session_keys:
            self.request.session.pop(key, None)

class AuthorizationView(FormView):
    template_name = 'Registration_app/registration_authorization.html'
    form_class = AuthorizationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = self.form_class.__name__
        context['title'] = 'Авторизація'
        context['subtitle'] = 'Ради тебе знову бачити!'
        context['view_type'] = 'authorization'
        return context

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        user = authenticate(self.request, username=email, password=password)

        if user is None:
            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(self.request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass

        if user is not None:
            if user.is_active:
                login(self.request, user)
                messages.success(self.request, f'Ласкаво просимо, {user.username}!')
                logger.info(f"User {user.username} logged in successfully")
                next_url = self.request.GET.get('next') or 'messenger_page'
                return redirect(next_url)
            else:
                messages.error(self.request, 'Обліковий запис не активовано. Перевірте вашу пошту для підтвердження.')
                form.add_error(None, 'Обліковий запис не активовано.')
                logger.warning(f"Inactive account login attempt: {email}")
                return self.form_invalid(form)
        else:
            messages.error(self.request, 'Невірна електронна пошта або пароль.')
            form.add_error(None, 'Невірна електронна пошта або пароль.')
            logger.warning(f"Failed login attempt for {email}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        logger.warning(f"Invalid authorization form: {form.errors}")
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('authorization')