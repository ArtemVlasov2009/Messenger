"""
URL configuration for Messenger project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import settings
from django.conf.urls.static import static
from Registration_app.views import CustomLogoutView
from Posts_app.views import PostsPageView
from Registration_app.views import RegistrationView, CodeConfirmationView, AuthorizationView
from Messenger_App.views import render_messenger_page  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', render_messenger_page, name='messenger_page'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('posts/', PostsPageView.as_view(), name='posts_page'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('confirm_code/', CodeConfirmationView.as_view(), name='confirm_code'),
    path('authorization/', AuthorizationView.as_view(), name='authorization'),
    path('messenger/', render_messenger_page, name='messenger'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
