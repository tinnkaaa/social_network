from django.http import JsonResponse
from django.views.generic import DetailView, View, TemplateView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from auth_system.models import User
from friends.services import follow_user, unfollow_user, is_following, can_view_profile, follow_request_sent

class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'friends/profile_detail.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        owner = self.get_object()
        viewer = self.request.user

        context['can_view_profile'] = can_view_profile(viewer, owner)
        context['is_following'] = is_following(viewer, owner)
        context['follow_request_sent'] = follow_request_sent(viewer, owner)

        if context['can_view_profile']:
            context['posts'] = owner.posts.select_related('author')
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