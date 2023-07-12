from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
import datetime
class UserForm(UserCreationForm):

    email = forms.EmailField(label='이메일')
    tel = forms.CharField(label='연락처')
    first_name = forms.CharField(label='성')
    last_name = forms.CharField(label='이름')
    gender = forms.CharField(label='성별')



    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "tel")


