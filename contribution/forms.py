from django import forms

from .models import NextOfKin


class NextOfKinForm(forms.ModelForm):
    class Meta:
        model = NextOfKin
        fields = ['first_name', 'last_name', 'sex', 'perc',
                  'telephone', 'address', 'city', 'photo', ]
