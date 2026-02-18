from django.core.exceptions import PermissionDenied
import json
from django.views import View
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy

from .models import Post, Comment, PostImage, Like
from .forms import PostForm, CommentForm
from .services import toggle_like, create_comment


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()

        files = self.request.FILES.getlist('images')
        for file in files:
            PostImage.objects.create(
                post=self.object,
                file=file
            )

        return redirect(self.object.get_absolute_url())


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object

        context['comments'] = post.comments.select_related('author')
        context['is_author'] = post.author == self.request.user
        context['liked'] = post.likes.filter(user=self.request.user).exists()

        return context


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['content']
    template_name = 'posts/post_form.html'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('profile')

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

class PostLikeView(LoginRequiredMixin, DetailView):
    model = Post

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        action = toggle_like(request.user, post)
        return JsonResponse({
            'liked': action == 'liked',
            'likes_count': post.likes.count()
        })

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        try:
            data = json.loads(request.body)
            text = data.get('text')
        except (json.JSONDecodeError, TypeError):
            text = request.POST.get('text')

        if not text:
            return JsonResponse({'error': 'Text is required.'}, status=400)

        comment = Comment.objects.create(
            post=post,
            author=request.user,
            text=text
        )

        post.comments_count = post.comments.count()
        post.save(update_fields=['comments_count'])

        return JsonResponse({
            'success': True,
            'comment_id': comment.id,
            'author': comment.author.username,
            'text': comment.text,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M'),
            'comments_count': post.comments_count
        })


class CommentDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)

        if comment.author != request.user and comment.post.author != request.user:
            raise PermissionDenied()

        post_id = comment.post.id
        comment.delete()
        return redirect('post_detail', pk=post_id)


class ToggleLikeView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(post=post, user=request.user)

        if not created:
            like.delete()
            liked = False
        else:
            liked = True

        return JsonResponse({
            'liked': liked,
            'likes_count': post.likes.count()
        })

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        self.object = form.save()

        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                "id": self.object.id,
                "author": self.object.author.username,
                "text": self.object.text,
                "comments_count": self.object.post.comments.count(),
            })
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user and comment.post.author != request.user:
            return redirect(comment.post.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.object.post.get_absolute_url()