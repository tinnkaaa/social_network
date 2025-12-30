from django.core.exceptions import PermissionDenied

class AdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_moderator():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)