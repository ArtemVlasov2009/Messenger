from django.shortcuts import render
from django.views.generic import ListView
from .models import User_Post

# Create your views here.
class PostsPageView(ListView):
    model = User_Post  # Предполагаю, что модель называется Post; замените на правильное имя, если нужно
    template_name = 'Posts_app/Posts.html'  # Путь к шаблону
    context_object_name = 'posts'  # Имя переменной в контексте шаблона

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'posts'  # Устанавливаем текущую страницу как 'posts'
        return context