from django.shortcuts import render

# Create your views here.
def render_messenger_page(request):
    return render(request, 'Messenger_App/Messenger.html')