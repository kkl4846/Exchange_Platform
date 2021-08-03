from django import forms
from . import models


class ForeignForm(forms.ModelForm):
    class Meta:
        model=models.Foreign
        fields='__all__'
  