
from django import forms
from django.contrib.auth.models import User

class EmailUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']