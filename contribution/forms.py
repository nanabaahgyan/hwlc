from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Sum


from .models import NextOfKin


class NextOfKinForm(forms.ModelForm):
    class Meta:
        model = NextOfKin
        fields = ['first_name', 'last_name', 'sex', 'perc',
                  'telephone', 'photo', 'address', 'city', 'country',]
