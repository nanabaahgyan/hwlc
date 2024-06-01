from django import forms

from .models import NextOfKin


class NextOfKinForm(forms.ModelForm):
    class Meta:
        model = NextOfKin
        fields = ['to_member', 'first_name', 'last_name', 'sex', 'perc',
                  'telephone', 'photo', 'address', 'city', 'country',]
        widgets = {'to_member': forms.HiddenInput(),
                   'address': forms.Textarea(attrs={'rows': 5})}
