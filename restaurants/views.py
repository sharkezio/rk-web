from django.shortcuts import render_to_response, render, get_object_or_404
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
from django.views.generic.edit import FormView, DeleteView, UpdateView
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied

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
    return (user.is_authenticated() and
            user.has_perm('restaurants.can_comment'))


class PermissionMixin(object):

    def get_object(self, *args, **kwargs):
        obj = super(PermissionMixin, self).get_object(*args, **kwargs)
        if not obj.visitor == str(self.request.user):
            # a = obj.visitor
            # b = str(self.request.user)
            # print "a", a
            # print "b", b
            # print "a == b", a == b
            # print "a is b", a is b
            # print "obj.visitor = ", obj.visitor
            # print "request.user = ", self.request.user
            # print "==", obj.visitor == self.request.user
            # print "is", obj.visitor is self.request.user
            raise PermissionDenied()
        else:
            return obj


class MenuView(DetailView):
    model = Restaurant
    template_name = 'menu.html'
    context_object_name = 'restaurant'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MenuView, self).dispatch(request, *args, **kwargs)

    # for redirect
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


# class CommentUpdateView(UpdateView):
#     model = Comment
#     form_class = CommentForm
#     # fields = ['visitor', 'email', 'content']
#     template_name = 'comment_update_form.html'

#     def get_object(self, *args, **kwargs):
#         obj = super(CommentUpdateView, self).get_object(*args, **kwargs)
#         if not obj.visitor == str(self.request.user):
#             raise PermissionDenied()
#         else:
#             return obj

#     def get_success_url(self):
#         return reverse('comment-view',
#                        kwargs={'pk': self.object.restaurant.pk})


class CommentUpdate(FormView, SingleObjectMixin):

    form_class = CommentForm
    template_name = 'comment_update_form.html'
    # success_url = '/index/'
    # initial = {'content': u'I don\'t have comment', 'visitor': u'temp'}

    model = Comment         # provide by SingleObjectMixin
    context_object_name = 'c'  # provide by SingleObjectMixin

    # pk=self.kwargs.get('pk')
    # self.objects.get(pk=self.kwargs.get('pk'))

    def get_success_url(self):
        self.object = self.get_object()
        # print 'Comment.restaurant.pk = ', Comment.restaurant.pk
        # print 'self.object.pk = ', self.object.restaurant.pk
        return reverse('comment-view',
                       kwargs={'pk': self.object.restaurant.pk})

    def get_initial(self):
        initial = super(CommentUpdate, self).get_initial()

        # self.object = self.get_object()
        comment = get_object_or_404(Comment, pk=self.kwargs.get('pk'))
        # comment = self.object.get(pk=self.kwargs.get('pk'))

        initial['visitor'] = comment.visitor
        initial['email'] = comment.email
        initial['content'] = comment.content
        # print "comment.visitor = ", comment.visitor
        # print "comment.email = ", comment.email
        # print "comment.content = ", comment.content

        return initial

    # def get_initial(self):
    #     initial = super(CommentView, self).get_initial()
    #     initial['visitor'] = self.request.user

    #     if self.request.user.is_authenticated():
    #         initial['email'] = self.request.user.email

    #     return initial

    def form_valid(self, form):

        comment = get_object_or_404(Comment, pk=self.kwargs.get('pk'))
        # comment = self.object.objects.get(pk=self.kwargs.get('pk'))
        c = Comment(
            id=self.kwargs.get('pk'),
            visitor=comment.visitor,
            email=form.cleaned_data['email'],
            content=form.cleaned_data['content'],
            date_time=timezone.localtime(timezone.now()),
            restaurant=comment.restaurant
        )
        c.save()

        c.userUpVotes.clear()    # reset votes duo to edit comment
        c.userDownVotes.clear()  # reset votes duo to edit comment
        # Comment.objects.create(
        #     visitor=form.cleaned_data['visitor'],
        #     email=form.cleaned_data['email'],
        #     content=form.cleaned_data['content'],
        #     date_time=timezone.localtime(timezone.now()),
        #     restaurant=self.get_object()
        #     # don't need to add vote cause many to many field
        # )

        # ----------->equal to below<-----------
        # context = self.get_context_data()
        # context['form'] = self.form_class(initial=self.initial)
        # return self.render_to_response(context)
        # ----------->equal to below<-----------
        # return self.render_to_response(self.get_context_data(
        #     form=self.form_class(initial=self.initial))
        # )
        return HttpResponseRedirect(self.get_success_url())
    # def get_context_data(self, **kwargs):
    #     self.object = self.get_object()
    #     return super(CommentView, self).get_context_data(
    #         object=self.object, **kwargs)

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super(CommentUpdate, self).get_context_data(
            object=self.object, **kwargs)

        return context

    def get_object(self, *args, **kwargs):
        obj = super(CommentUpdate, self).get_object(*args, **kwargs)
        if not obj.visitor == str(self.request.user):
            raise PermissionDenied()
        else:
            return obj


class CommentDelete(DeleteView):
    model = Comment
    # success_url = reverse_lazy('restaurants-list')
    # success_url = HttpResponseRedirect("request.get_full_path()")

    def get_object(self, *args, **kwargs):
        obj = super(CommentDelete, self).get_object(*args, **kwargs)
        if not obj.visitor == str(self.request.user):
            raise PermissionDenied()
        else:
            return obj

    def get_success_url(self):
        return reverse('comment-view',
                       kwargs={'pk': self.object.restaurant.pk})


class CommentView(FormView, SingleObjectMixin):

    form_class = CommentForm
    template_name = 'comments.html'
    # success_url = '/comment/'
    # success_url = '/index/'
    # initial = {'content': u'I don\'t have comment', 'visitor': u'temp'}

    model = Restaurant         # provide by SingleObjectMixin
    context_object_name = 'r'  # provide by SingleObjectMixin

    # def get_queryset(self):
    #     restaurant = Restaurant.objects.get(pk=self.kwargs.get('pk'))
    #     comments = restaurant.comment_set.all()
    #     for c in comments:
    #         c.userUpVotes = c.userUpVotes.filter(
    #             id=self.request.user.id).count()
    #         c.userDownVotes = c.userDownVotes.filter(
    #             id=self.request.user.id).count()
    #     return comments

    def get_success_url(self):
        return reverse('comment-view',
                       kwargs={'pk': self.kwargs.get('pk')})

    def get_initial(self):
        initial = super(CommentView, self).get_initial()
        initial['visitor'] = self.request.user

        if self.request.user.is_authenticated():
            initial['email'] = self.request.user.email

        return initial

    def form_valid(self, form):
        Comment.objects.create(
            visitor=form.cleaned_data['visitor'],
            email=form.cleaned_data['email'],
            content=form.cleaned_data['content'],
            date_time=timezone.localtime(timezone.now()),
            restaurant=self.get_object()
            # don't need to add vote cause many to many field
        )

        # ----------->equal to below<-----------
        # context = self.get_context_data()
        # context['form'] = self.form_class(initial=self.initial)
        # return self.render_to_response(context)
        # ----------->equal to below<-----------
        # return self.render_to_response(self.get_context_data(
        #     form=self.form_class(initial=self.initial))
        # )
        # return HttpResponseRedirect("")
        return HttpResponseRedirect(self.get_success_url())
    # def get_context_data(self, **kwargs):
    #     self.object = self.get_object()
    #     return super(CommentView, self).get_context_data(
    #         object=self.object, **kwargs)

    def get_context_data(self, **kwargs):  # overide context_object_name var
        self.object = self.get_object()
        context = super(CommentView, self).get_context_data(
            object=self.object, **kwargs)

        # thread = get_object_or_404(Comment, pk=23)
        # # thread = get_object_or_404(Comment, pk=self.kwargs.get('pk'))

        # thisUserUpVote = thread.userUpVotes.filter(
        #     id=self.request.user.id).count()
        # context['thisUserUpVote'] = thisUserUpVote

        # thisUserDownVote = thread.userDownVotes.filter(
        #     id=self.request.user.id).count()
        # context['thisUserDownVote'] = thisUserDownVote

        # num_votes = thread.userUpVotes.count() - thread.userDownVotes.count()
        # context['num_votes'] = num_votes

        return context

    def get_object(self, queryset=None):
        obj = super(CommentView, self).get_object(queryset=queryset)
        # print obj
        # restaurant = self.object
        # print restaurant
        # restaurant = Restaurant.objects.get(pk=self.kwargs.get('pk'))
        # print restaurant

        # comments = self.object.comment_set.all()
        comments = obj.comment_set.all()
        # print comments
        for c in comments:
            c.thisUserUpVote = c.userUpVotes.filter(
                id=self.request.user.id).count()
            c.thisUserDownVote = c.userDownVotes.filter(
                id=self.request.user.id).count()
            # print c
            # print "thisUserUpVote", c.thisUserUpVote
            # print "thisUserDownVote", c.thisUserDownVote
            c.save()
        #     context['thisUserUpVote'] = thisUserUpVote
        #     context['thisUserDownVote'] = thisUserDownVote
        return obj

    # -----if user.has_perm('restaurants.can_comment') required-----
    # @method_decorator(user_passes_test(user_can_comment,
    #                                    login_url='/accounts/login/'))
    # def dispatch(self, request, *args, **kwargs):
    #     return super(CommentView, self).dispatch(request, *args, **kwargs)
    # -----if user.has_perm('restaurants.can_comment') required-----


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


def vote(request):
    # thread_id = 23
    thread_id = int(request.POST.get('id'))
    vote_type = request.POST.get('type')
    vote_action = request.POST.get('action')
    # print "thread_id = ", thread_id
    # print "vote_type = ", vote_type
    # print "vote_action = ", vote_action

    # thread = get_object_or_404(Thread, pk=thread_id)
    thread = get_object_or_404(Comment, pk=thread_id)

    thisUserUpVote = thread.userUpVotes.filter(id=request.user.id).count()
    # print "thisUserUpVote", thisUserUpVote
    thisUserDownVote = thread.userDownVotes.filter(id=request.user.id).count()
    # print "thisUserDownVote", thisUserDownVote

    if (vote_action == 'vote'):
        if (thisUserUpVote == 0) and (thisUserDownVote == 0):
            if (vote_type == 'up'):
                # print "userUpVotes.add"
                thread.userUpVotes.add(request.user)
            elif (vote_type == 'down'):
                thread.userDownVotes.add(request.user)
            else:
                # print "error-unknown vote type"
                return HttpResponse('error-unknown vote type')
        else:
            # print "error - already voted"
            return HttpResponse('error - already voted')
    elif (vote_action == 'recall-vote'):
        if (vote_type == 'up') and (thisUserUpVote == 1):
            # print "userUpVotes.remove"
            thread.userUpVotes.remove(request.user)
        elif (vote_type == 'down') and (thisUserDownVote == 1):
            thread.userDownVotes.remove(request.user)
        else:
            # print "error - unknown vote type or no vote to recall"
            return HttpResponse(
                'error - unknown vote type or no vote to recall')
    else:
        # print "error - bad action"
        return HttpResponse('error - bad action')

    num_votes = thread.userUpVotes.count() - thread.userDownVotes.count()

    thisUserUpVote = thread.userUpVotes.filter(id=request.user.id).count()
    # print "thisUserUpVote = ", thisUserUpVote
    thisUserDownVote = thread.userDownVotes.filter(id=request.user.id).count()
    # print "thisUserDownVote = ", thisUserDownVote

    # print "num_votes = ", num_votes
    # print "Here !!!!!!num_votes"

    return HttpResponse(num_votes)
    # return render(request, 'comments.html', {"num_votes": num_votes})


def meta(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>{0}</td><td>{1}</td></tr>'.format(k, v))
    return HttpResponse('<table>{0}</table>'.format('\n'.join(html)))


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
