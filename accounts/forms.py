from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')
        labels = {
            'username': _('Username'),
            'email': _('Email'),
        }