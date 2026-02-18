from allauth.account.adapter import DefaultAccountAdapter
from .models import Profile


class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)

        if commit:
            user.save()
            Profile.objects.get_or_create(user=user)

        return user