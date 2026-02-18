from django.shortcuts import render, redirect
from django.views.generic import UpdateView, DetailView
from django.urls import reverse_lazy
from .models import Profile, User
from posts.models import Post
from django.contrib.auth.mixins import LoginRequiredMixin

class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'account/profile/detail.html'

    def get_object(self):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['followers_count'] = user.profile.followers_count
        context['following_count'] = user.profile.following_count
        context['posts'] = Post.objects.filter(author=self.request.user).prefetch_related('images')
        return context

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['avatar', 'bio', 'gender', 'phone_number', 'is_private']
    template_name = 'account/profile/update.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user.profile
