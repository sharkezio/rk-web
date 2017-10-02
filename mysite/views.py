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


# def menu(request):
#     restaurants = Restaurant.objects.all()
#     return render_to_response('menu.html', locals())


def welcome(request):
    if 'user_name' in request.GET and request.GET['user_name'] != '':
        return HttpResponse('Welcome!~' + request.GET['user_name'])
    else:
        return render_to_response('welcome.html', locals())


# def costum_login(request):
#     if request.user.is_authenticated():
#         return HttpResponseRedirect('/index/')
#     else:
#         return auth.views.login(request)

# def login(request):

#     if request.user.is_authenticated():
#         return HttpResponseRedirect('/index/')

#     username = request.POST.get('username', '')
#     password = request.POST.get('password', '')

#     user = auth.authenticate(username=username, password=password)

#     if user is not None and user.is_active:
#         auth.login(request, user)
#         return HttpResponseRedirect('/index/')
#     else:
#         return render_to_response('login.html',
#                                   RequestContext(request, locals()))

# def custom_login(request):
#     form = LoginForm(request.POST or None)
#     if request.POST and form.is_valid():
#         user = form.login(request)
#         if user:
#             auth.login(request, user)
#             return HttpResponseRedirect("/index/")  # redirect to success page
#     return render(request, 'login.html', {'form': form})

def custom_login(request):
    form = LoginForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            user = form.login(request)
            if user:
                auth.login(request, user)
                # return HttpResponseRedirect("/index/")  # redirect success page
                return HttpResponseRedirect(reverse('index'))
        else:  # if form isn't valid refill username to user login page
            username = request.POST.get('username', '')
            context = {
                'form': form,
                'username': username
            }
            return render(request, 'login.html', context)
    return render(request, 'login.html', {'form': form})


# def index(request):
#     return render_to_response('index.html',
#                               RequestContext(request, locals()))


class IndexView(TemplateView):
    template_name = 'index.html'

# # overwrite get() to use ContextMixin from TemplateView to set request variable

#     def get(self, request, *args, **kwargs):
#         context = self.get_context_data(**kwargs)
#         context['request'] = request
#         return self.render_to_response(context)


def logout(request):
    auth.logout(request)
    # return HttpResponseRedirect('/index/')
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        form = UserCreateEmailForm(request.POST)
        if form.is_valid():
            # user = form.save()
            form.save()
            # return HttpResponseRedirect('/accounts/login/')
            return HttpResponseRedirect(reverse('accounts-login'))
    else:
        # form = UserCreationForm()
        form = UserCreateEmailForm()
    # return render_to_response('register.html',
    #                           RequestContext(request, locals()))
    return render(request, 'register.html', {'form': form})
