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
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView, RedirectView


# --import all module in order to call full view function name--
import django.contrib.auth.views
import views
import restaurants.views

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^menu/(?P<pk>\d+)/$', restaurants.views.MenuView.as_view()),
    url(r'^restaurants_list/$',
        login_required(restaurants.views.RestaurantsView.as_view()),
        name='restaurants-list'),
    url(r'^users_list/$', login_required(restaurants.views.list_users)),
    url(r'^comment/(?P<pk>\d+)/$',
        restaurants.views.CommentView.as_view(), name='comment-view'),
    url(r'^accounts/login/$', views.custom_login, name='accounts-login'),
    url(r'^accounts/logout/$', django.contrib.auth.views.logout,
        name='accounts-logout'),
    url(r'^welcome/$', views.welcome),
    url(r'^vote/$', restaurants.views.vote),
    url(r'^update/comment/(?P<pk>\d+)/$',
        restaurants.views.CommentUpdate.as_view(), name='comment-update'),
    url(r'^delete/comment/(?P<pk>\d+)/$',
        restaurants.views.CommentDelete.as_view(), name='comment-delete'),
    url(r'^$',
        TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^accounts/register/$', views.register),
    # url(r'^favicon\.ico$',
    #     RedirectView.as_view(url='/static/favicons/favicon.ico',
    #                          permanent=True)),
    url(r'^android-chrome-192x192\.png$',
        RedirectView.as_view(url='/static/favicons/android-chrome-192x192.png',
                             permanent=True)),
    url(r'^android-chrome-512x512\.png$',
        RedirectView.as_view(url='/static/favicons/android-chrome-512x512.png',
                             permanent=True)),
    url(r'^browserconfig\.xml$',
        RedirectView.as_view(url='/static/favicons/browserconfig.xml',
                             permanent=True)),
]

if settings.DEBUG:  # for practice usage
    urlpatterns += [
        url(r'^meta/$', restaurants.views.meta),
        url(r'^set_c/$', restaurants.views.set_c),
        url(r'^get_c/$', restaurants.views.get_c),
        url(r'^use_session/$', restaurants.views.use_session),
        url(r'^session_test/$', restaurants.views.session_test),
    ]
