from django.http import JsonResponse
from django.views.generic import DetailView, View, TemplateView, ListView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from auth_system.models import User
from .models import Follow
from .services import follow_user, unfollow_user, is_following, can_view_profile, follow_request_sent
from posts.models import Post

class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'friends/profile_detail.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def dispatch(self, request, *args, **kwargs):
        if kwargs['username'] == request.user.username:
            return redirect('profile')
        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        owner = self.get_object()
        viewer = self.request.user

        context['can_view_profile'] = can_view_profile(viewer, owner)
        context['is_following'] = is_following(viewer, owner)
        context['follow_request_sent'] = follow_request_sent(viewer, owner)

        if context['can_view_profile']:
            context['posts'] = Post.objects.filter(
                author=owner,
                is_active=True
            )
        else:
            context['posts'] = []

        return context

class FollowActionView(LoginRequiredMixin, View):
    def post(self, request, username):
        target = get_object_or_404(User, username=username)
        actor = request.user

        if target == actor:
            return JsonResponse({'error': 'self'}, status=400)

        if is_following(actor, target):
            result = unfollow_user(actor, target)
        else:
            result = follow_user(actor, target)

        target.profile.refresh_from_db()

        return JsonResponse({
            'result': result,
            'followers_count': target.profile.followers_count
        })

class FollowersListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'friends/followers_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        return user.profile.followers()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner'] = get_object_or_404(User, username=self.kwargs['username'])
        context['can_remove'] = self.request.user == context['owner']
        return context

class FollowingListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'friends/following_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        return user.profile.following()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner'] = get_object_or_404(User, username=self.kwargs['username'])
        context['viewer'] = self.request.user
        return context


class UserSearchApiView(LoginRequiredMixin, View):
    def get(self, request):
        q = request.GET.get('q', '').strip()

        if len(q) < 2:
            return JsonResponse({'results': []})

        users = User.objects.filter(
            username__icontains=q
        ).exclude(id=request.user.id)[:10]

        data = []
        for u in users:
            data.append({
                'username': u.username,
                'avatar': u.profile.avatar.url if u.profile.avatar else '/static/avatar.png',
                'url': f'/u/{u.username}/'
            })

        return JsonResponse({'results': data})