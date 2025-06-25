from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .models import Post, Link, Image
from .forms import PostForm
from Messenger_App.models import Profile
import logging

logger = logging.getLogger(__name__)

class PostsPageView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'Posts_app/Posts.html'
    context_object_name = 'user_posts'
    ordering = ['-id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'posts'
        context['form'] = context.get('form', PostForm())
        return context

    def post(self, request, *args, **kwargs):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        form = PostForm(request.POST, request.FILES)
        
        if form.is_valid():
            post = form.save(commit=False)
            post.author = get_object_or_404(Profile, user=request.user)
            post.save()
            form.save_m2m()
            uploaded_images = request.FILES.getlist('images_upload')
            for f in uploaded_images:
                image_instance = Image.objects.create(file=f, owner=post.author, filename=f.name)
                post.images.add(image_instance)
            
            article_link = form.cleaned_data.get('article_link')
            if article_link:
                Link.objects.create(url=article_link, post=post)

            for key, value in request.POST.items():
                if key.startswith('extra_link_') and value.strip():
                    Link.objects.create(url=value.strip(), post=post)

            if is_ajax:
                return JsonResponse({'status': 'success', 'message': 'Пост успішно створено.'})
            return redirect('posts_page')
        else:
            if is_ajax:
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
            self.object_list = self.get_queryset()
            context = self.get_context_data(object_list=self.object_list)
            context['form'] = form
            return self.render_to_response(context)

def delete_post(request, post_id):
    if request.method == 'POST' and request.user.is_authenticated:
        post = get_object_or_404(Post, id=post_id)
        if post.author.user == request.user:
            post.delete()
            return JsonResponse({'status': 'success', 'message': 'Пост успішно видалено.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Ви не маєте права видаляти цей пост'}, status=403)
    return JsonResponse({'status': 'error', 'message': 'Невірний метод запиту'}, status=400)

def delete_link(request, post_id):
    if request.method == 'POST' and request.user.is_authenticated:
        post = get_object_or_404(Post, id=post_id)
        if post.author.user != request.user:
            return JsonResponse({'status': 'error', 'message': 'Ви не маєте права видаляти посилання цього поста'}, status=403)
        
        link_url = request.POST.get('link_url')
        if not link_url:
            return JsonResponse({'status': 'error', 'message': 'Не вказано посилання для видалення'}, status=400)
        
        try:
            link = Link.objects.get(url=link_url, post=post)
            link.delete()
            return JsonResponse({'status': 'success', 'message': 'Посилання успішно видалено.'})
        except Link.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Посилання не знайдено'}, status=404)
        except Exception as e:
            logger.error(f"Error deleting link {link_url} for post {post_id}: {e}")
            return JsonResponse({'status': 'error', 'message': 'Помилка при видаленні посилання'}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Невірний метод запиту'}, status=400)

def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author.user != request.user:
        return JsonResponse({'status': 'error', 'message': 'Ви не маєте права редагувати цей пост'}, status=403)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            form.save_m2m()

            uploaded_images = request.FILES.getlist('images_upload')
            for f in uploaded_images:
                image_instance = Image.objects.create(file=f, owner=post.author, filename=f.name)
                post.images.add(image_instance)

            Link.objects.filter(post=post).delete()
            article_link = form.cleaned_data.get('article_link')
            if article_link:
                Link.objects.create(url=article_link, post=post)

            for key, value in request.POST.items():
                if key.startswith('extra_link_') and value.strip():
                    Link.objects.create(url=value.strip(), post=post)

            return JsonResponse({'status': 'success', 'message': 'Пост успішно оновлено.'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        tags_list = list(post.tags.values_list('name', flat=True))
        links = Link.objects.filter(post=post)
        images = post.images.all()
        return JsonResponse({
            'status': 'success',
            'title': post.title or '',
            'content': post.content or '',
            'tags': tags_list,
            'article_link': links.first().url if links.exists() else '',
            'images': [image.file.url for image in images],
        })