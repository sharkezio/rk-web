from django.shortcuts import render_to_response, render
from django.http import HttpResponse
from django.http import HttpResponseRedirect, Http404
from django.utils import timezone
from django.template import RequestContext
from django.contrib.sessions.models import Session
from django.contrib import auth
from django.contrib.auth.decorators import (login_required,
                                            user_passes_test,
                                            permission_required)
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView

from restaurants.models import Restaurant, Comment, Food
from restaurants.forms import CommentForm


# @login_required
# def list(request, model):
#     objs = model.objects.all()
#     users = model.objects.all()
#     return render(
#         request,
#         '{0}s_list.html'.format(model.__name__.lower()),
#         locals()
#     )


# @login_required
def list_users(request):
    users = auth.models.User.objects.all()
    return render(request, 'users_list.html', locals())
    # return render_to_response('users_list.html',
    #                           RequestContext(request, locals()))


def user_can_comment(user):
    return (user.is_authenticated and
            user.has_perm('restaurants.can_comment'))


class MenuView(DetailView):
    model = Restaurant
    template_name = 'menu.html'
    context_object_name = 'restaurant'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MenuView, self).dispatch(request, *args, **kwargs)

    def get(self, request, pk, *args, **kwargs):
        try:
            return super(MenuView, self).get(self, request, pk=pk,
                                             *args, **kwargs)
        except Http404:
            return HttpResponseRedirect('/restaurants_list/')

# def menu(request):
#     # path = request.path
#     # restaurants = Restaurant.objects.all()
#     # restaurant = Restaurant.objects.get(id=2)
#     # return render_to_response('menu.html', locals())
#     if 'id' in request.GET and request.GET['id'] != '':
#         restaurant = Restaurant.objects.get(id=request.GET['id'])
#         return render_to_response('menu.html', locals())
#     else:
#         return HttpResponseRedirect("/restaurants_list/")


def meta(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>{0}</td><td>{1}</td></tr>'.format(k, v))
    return HttpResponse('<table>{0}</table>'.format('\n'.join(html)))


class RestaurantsView(ListView):
    model = Restaurant
    template_name = 'restaurants_list.html'
    context_object_name = 'restaurants'


# def list_restaurants(request):
#     restaurants = Restaurant.objects.all()
#     # try to use session to store model object
#     # request.session['restaurants'] = restaurants
#     print request.user.user_permissions.all()
#     # return render_to_response('restaurants_list.html', locals())
#     # return render_to_response('restaurants_list.html',
#     #                           RequestContext(request, locals()))
#     return render(request, 'restaurants_list.html', locals())


class CommentView(FormView, SingleObjectMixin):

    form_class = CommentForm
    template_name = 'comments.html'
    success_url = '/comment/'
    initial = {'content': u'I don\'t have comment'}
    model = Restaurant
    context_object_name = 'r'

    def form_valid(self, form):
        Comment.objects.create(
            visitor=form.cleaned_data['visitor'],
            email=form.cleaned_data['email'],
            content=form.cleaned_data['content'],
            date_time=timezone.localtime(timezone.now()),
            restaurant=self.get_object()
        )
        return self.render_to_response(self.get_context_data(
            form=self.form_class(initial=self.initial))
        )

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        return super(CommentView, self).get_context_data(
            object=self.object, **kwargs)

    @method_decorator(user_passes_test(user_can_comment,
                                       login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(CommentView, self).dispatch(request, *args, **kwargs)

# def comment(request, restaurant_id):
#     if restaurant_id:
#         r = Restaurant.objects.get(id=restaurant_id)
#     else:
#         return HttpResponseRedirect("/restaurants_list/")
#         # may not enter forever
#         # cause restaurant_id need

#     errors = []
#     if request.POST:
#         visitor = request.POST['visitor']
#         content = request.POST['content']
#         email = request.POST['email']
#         date_time = timezone.localtime(timezone.now())
#         if any(not request.POST[k] for k in request.POST):
#             errors.append('* blank column, please retype')
#         if request.POST['email']:
#             if '@' not in email:
#                 errors.append('* email format wrong, please retype')
#         if not errors:
#             Comment.objects.create(visitor=visitor, email=email,
#                                    content=content, date_time=date_time,
#                                    restaurant=r)
#             visitor, email, content = ('', '', '')
#         f = CommentForm()
#     return render_to_response('comments.html',
#                               RequestContext(request, locals()))



# # @user_passes_test(user_can_comment, login_url='/accounts/login/')
# @permission_required('restaurants.can_comment', login_url='/accounts/login/')
# def comment(request, restaurant_id):
#     if restaurant_id:
#         r = Restaurant.objects.get(id=restaurant_id)
#     else:
#         return HttpResponseRedirect("/restaurants_list/")
#         # may not enter forever
#         # cause restaurant_id need

#     if request.POST:
#         f = CommentForm(request.POST)
#         if f.is_valid():
#             visitor = f.cleaned_data['visitor']
#             content = f.cleaned_data['content']
#             email = f.cleaned_data['email']
#             date_time = timezone.localtime(timezone.now())

#             c = Comment.objects.create(visitor=visitor, email=email,
#                                        content=content, date_time=date_time,
#                                        restaurant=r)
#             f = CommentForm(initial={'content': 'No Comment.'})
#     else:
#         f = CommentForm(initial={'content': 'No Comment.'})
#     return render_to_response('comments.html',
#                               RequestContext(request, locals()))


def set_c(request):
    response = HttpResponse('Set your lucky number as 8')
    response.set_cookie('lucky_number', 8)
    return response


def get_c(request):
    if 'lucky_number' in request.COOKIES:
        return HttpResponse('Your lucky number is {0}'.format(
                            request.COOKIES['lucky_number']))
    else:
        return HttpResponse('No Cookies.')


def use_session(request):
    request.session['lucky_number'] = 8  # set lucky number
    if 'lucky_number' in request.session:
        lucky_number = request.session['lucky_number']
        # read lucky number
        response = HttpResponse('Your lucky number is ' + str(lucky_number))
    del request.session['lucky_number']  # delete lucky number
    return response


def session_test(request):
    sid = request.COOKIES['sessionid']
    sid2 = request.session.session_key
    s = Session.objects.get(pk=sid)
    s_info = ('Session ID:' + sid + '<br>SessionID2:' + sid2 +
              '<br>Expire_date:' + str(s.expire_date) + '<br>Data:' +
              str(s.get_decoded()))
    return HttpResponse(s_info)
