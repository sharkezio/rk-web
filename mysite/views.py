from django.shortcuts import render_to_response, render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.base import View, TemplateView
from django.core.urlresolvers import reverse

from restaurants.models import Restaurant
from forms import LoginForm, UserCreateEmailForm


def welcome(request):
    if 'user_name' in request.GET and request.GET['user_name'] != '':
        return HttpResponse('Welcome!~' + request.GET['user_name'])
    else:
        return render_to_response('welcome.html', locals())


def custom_login(request):
    form = LoginForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            user = form.login(request)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
        else:  # if form isn't valid refill username to user login page
            username = request.POST.get('username', '')
            context = {
                'form': form,
                'username': username
            }
            return render(request, 'login.html', context)
    return render(request, 'login.html', {'form': form})


class IndexView(TemplateView):
    template_name = 'index.html'


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == 'POST':
        form = UserCreateEmailForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('accounts-login'))
    else:
        form = UserCreateEmailForm()
    return render(request, 'register.html', {'form': form})
