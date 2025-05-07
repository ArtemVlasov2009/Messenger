from django.shortcuts import render
from .forms import AuthorizationForm

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
    else:
        form = AuthorizationForm()

    return render(request, 'Messenger_App/authorization.html', {'form': form})