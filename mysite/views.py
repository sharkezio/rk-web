from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.base import View, TemplateView

from restaurants.models import Restaurant


def menu(request):
    restaurants = Restaurant.objects.all()
    return render_to_response('menu.html', locals())


def welcome(request):
    if 'user_name' in request.GET and request.GET['user_name'] != '':
        return HttpResponse('Welcome!~' + request.GET['user_name'])
    else:
        return render_to_response('welcome.html', locals())


def login(request):

    if request.user.is_authenticated():
        return HttpResponseRedirect('/index/')

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = auth.authenticate(username=username, password=password)

    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect('/index/')
    else:
        return render_to_response('login.html',
                                  RequestContext(request, locals()))


# def index(request):
#     return render_to_response('index.html',
#                               RequestContext(request, locals()))


class IndexView(TemplateView):
    template_name = 'index.html'

#     def get(self, request, *args, **kwargs):
#         context = self.get_context_data(**kwargs)
#         context['request'] = request
#         return self.render_to_response(context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/index/')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect('/accounts/login/')
    else:
        form = UserCreationForm()
    return render_to_response('register.html',
                              RequestContext(request, locals()))
