"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin, auth
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView

# --import specified view function from module--
# from django.contrib.auth.views import login, logout

# from views import welcome, index, register
# from restaurants.views import menu, meta, list_restaurants, comment, set_c, \
#     get_c, session_test, use_session


# admin.autodiscover()

# urlpatterns = [
#     url(r'^admin/', include(admin.site.urls)),
#     url(r'^menu/$', menu),
#     url(r'^meta/$', meta),
#     url(r'^welcome/$', welcome),
#     url(r'^restaurants_list/$', login_required(list_restaurants)),
#     url(r'^comment/(\d{1,5})/$', comment),
#     url(r'^set_c/$', set_c),
#     url(r'^get_c/$', get_c),
#     url(r'^use_session/$', use_session),
#     url(r'^session_test/$', session_test),
#     # url(r'^accounts/login/$', login),
#     url(r'^accounts/login/$', login, {'template_name': 'login.html'}),
#     url(r'^accounts/logout/$', logout),
#     url(r'^index/$', index),
#     url(r'^accounts/register/$', register)
# ]


# # --import all module in order to call full view function name--
import django.contrib.auth.views

import views

import restaurants.views

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^menu/(?P<pk>\d+)/$', restaurants.views.MenuView.as_view()),
    # url(r'^menu/$', restaurants.views.menu),
    # url(r'^menu/(?P<id>\d{1,5})/$', restaurants.views.menu),

    url(r'^restaurants_list/$',
        login_required(restaurants.views.RestaurantsView.as_view())),
    # url(r'^restaurants_list/$',
    #     login_required(restaurants.views.list_restaurants)),
    # url(r'^restaurants_list/$', restaurants.views.list,
    #     {'model': restaurants.models.Restaurant}),

    url(r'^users_list/$',
        login_required(restaurants.views.list_users)),
    # url(r'^users_list/$', restaurants.views.list,
    #     {'model': auth.models.User}),

    url(r'^comment/(?P<pk>\d+)/$', restaurants.views.CommentView.as_view()),
    # url(r'^comment/(?P<restaurant_id>\d{1,5})/$', restaurants.views.comment),
    # url(r'^comment/(\d{1,5})/$', restaurants.views.comment),

    # url(r'^accounts/login/$', login, {'template_name': 'login.html'}),
    url(r'^accounts/login/$', django.contrib.auth.views.login),
    url(r'^accounts/logout/$', django.contrib.auth.views.logout),

    url(r'^welcome/$', views.welcome),
    # url(r'^index/$', views.index),
    # url(r'^index/$', views.IndexView.as_view()),
    url(r'^index/$',
        TemplateView.as_view(template_name='index.html')),
    url(r'^accounts/register/$', views.register)
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^meta/$', restaurants.views.meta),
        url(r'^set_c/$', restaurants.views.set_c),
        url(r'^get_c/$', restaurants.views.get_c),
        url(r'^use_session/$', restaurants.views.use_session),
        url(r'^session_test/$', restaurants.views.session_test),
    ]
