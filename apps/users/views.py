from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from .models import User

# Create your views here.
def index(request):
    if 'user' in request.session:
        return redirect(reverse('travels:index'))

    return render(request, 'users/index.html')

def register(request):
    if request.method == "POST":

        response = User.objects.register(request.POST)

        if type(response) is list:
            for error in response:
                messages.error(request, error)

            return redirect(reverse('users:index'))
        else:
            user = {
                'id': response.id,
                'username': response.username
            }
            request.session['user'] = user
            return redirect(reverse('travels:index'))

def login(request):
    if request.method == "POST":

        response = User.objects.login(request.POST)

        if type(response) is list:
            for error in response:
                messages.error(request, error)

            return redirect(reverse('users:index'))
        else:
            user = {
                'id': response.id,
                'username': response.username
            }
            request.session['user'] = user
            return redirect(reverse('travels:index'))

def logout(request):
    if 'user' in request.session:
        request.session.pop('user')

    return redirect(reverse('users:index'))
