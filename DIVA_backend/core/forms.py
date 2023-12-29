from django import forms
from .models import Voter

class VoterRegisterForm(forms.ModelForm):
    class Meta:
        model = Voter
        fields = ['name','contact','email','otp']

    email = forms.EmailField(required = False)