from django import forms
from django.contrib.auth import get_user_model

from .models import UserProfile


class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = []
        # fields = ['first_name', 'last_name', 'email']


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['telephone', 'date_of_birth', 'photo',
                  'bank_name', 'bank_acct_no', 'bank_acct_branch']
