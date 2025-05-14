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
from Messenger_App.views import render_messenger_page, render_authorization_page
from Registration_app.views import render_registration_page
from Messenger_App.views import CustomLogoutView
from django.views.generic import TemplateView, ListView
from Posts_app.views import PostsPageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', render_messenger_page, name='messenger_page'),
    path('authorization/', render_authorization_page, name='authorization_page'),
    path('registration/', render_registration_page.as_view(), name='registration_page'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('posts/', PostsPageView.as_view(), name='posts_page'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)