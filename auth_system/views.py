from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from .forms import RegisterForm, ProfileForm
from .models import Profile, User
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'auth_system/register.html'
    success_url = reverse_lazy('login')

class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'auth_system/profile/detail.html'

    def get_object(self):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['followers_count'] = user.profile.followers_count
        context['following_count'] = user.profile.following_count
        return context

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'auth_system/profile/update.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user.profile
