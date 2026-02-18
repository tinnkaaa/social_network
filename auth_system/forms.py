from allauth.account.forms import SignupForm
from django import forms


class CustomSignupForm(SignupForm):
    gender = forms.ChoiceField(
        choices=[('male', 'Male'), ('female', 'Female')],
        required=False
    )
    phone_number = forms.CharField(required=False)

    def save(self, request):
        user = super().save(request)
        profile = user.profile

        profile.gender = self.cleaned_data.get('gender')
        profile.phone_number = self.cleaned_data.get('phone_number')
        profile.save()

        return user