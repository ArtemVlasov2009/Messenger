from django.shortcuts import render
from django.views.generic import ListView
from .models import User_Post

# Create your views here.
class PostsPageView(ListView):
    model = User_Post  
    template_name = 'Posts_app/Posts.html'  
    context_object_name = 'posts' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'posts'  
        return context