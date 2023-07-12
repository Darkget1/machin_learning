from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from common.forms import UserForm
from django.utils import timezone
from datetime import datetime


def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            form.create_date = timezone.now()
            login(request, user)
            return redirect('common:profile')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})

