from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User_Post
from .forms import PostForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

class PostsPageView(LoginRequiredMixin, ListView):
    model = User_Post
    template_name = 'Posts_app/Posts.html'
    context_object_name = 'user_posts'
    ordering = ['-id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'posts'
        context['form'] = context.get('form', PostForm())
        return context

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts_page')
        else:
            self.object_list = self.get_queryset()
            context = self.get_context_data(object_list=self.object_list)
            context['form'] = form
            return self.render_to_response(context)

def delete_post(request, post_id):
    if request.method == 'POST' and request.user.is_authenticated:
        post = get_object_or_404(User_Post, id=post_id)
        if post.user == request.user:
            post.delete()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Ви не маєте права видаляти цей пост'}, status=403)
    return JsonResponse({'status': 'error', 'message': 'Невірний метод запиту'}, status=400)