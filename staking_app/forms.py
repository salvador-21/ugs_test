from django import forms
import django.forms.utils
import django.forms.widgets
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import StakeSlot,StakeLogs
from django.contrib.auth.password_validation import validate_password
from django.core import validators

# from django_recaptcha.fields import ReCaptchaField
# from django_recaptcha.widgets import ReCaptchaV2Invisible

class StakeForm(ModelForm):
    s_name=forms.CharField(label='Stake Name', widget=forms.TextInput(attrs={'maxlength':'2','placeholder':'0','class':'form-control stake_name'}))
    s_rate=forms.IntegerField(label='Stake Rate Percentage', widget=forms.NumberInput(attrs={'maxlength':'2','placeholder':'0','class':'form-control stake_rate'}))
    s_amount=forms.IntegerField(label='Stake Amount', widget=forms.NumberInput(attrs={'maxlength':'2','placeholder':'0','class':'form-control '}))

    class Meta:
        model = StakeSlot
        fields=('s_name','s_rate','s_amount',)
