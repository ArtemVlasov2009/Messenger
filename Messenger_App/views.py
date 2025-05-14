from django.shortcuts import render, redirect
from .forms import AuthorizationForm
from django.contrib.auth.views import LogoutView
from Posts_app.models import User_Post

# Create your views here.
def render_messenger_page(request):
    return render(request, 'Messenger_App/Messenger.html', {'current_page': 'home'})

def render_authorization_page(request):
    if request.method == 'POST':
        form = AuthorizationForm(request.POST)
        if form.is_valid():
            # тут логика авторизации
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            verification = form.cleaned_data['email_verification']
            # ...
            return redirect('/')
    else:
        form = AuthorizationForm()

    return render(request, 'Messenger_App/authorization.html', {'form': form})


class CustomLogoutView(LogoutView):
    next_page = 'authorization_page'