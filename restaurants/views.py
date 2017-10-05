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


def list_users(request):
    users = auth.models.User.objects.all()
    return render(request, 'users_list.html', locals())


def user_can_comment(user):
    return (user.is_authenticated() and
            user.has_perm('restaurants.can_comment'))


class PermissionMixin(object):  # require request.user match comment creater

    def get_object(self, *args, **kwargs):
        obj = super(PermissionMixin, self).get_object(*args, **kwargs)

        if not obj.visitor == self.request.user.username:
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

    def get(self, request, pk, *args, **kwargs):
        try:
            return super(MenuView, self).get(self, request, pk=pk,
                                             *args, **kwargs)
        except Http404:
            return HttpResponseRedirect('/restaurants_list/')


class RestaurantsView(ListView):

    model = Restaurant
    template_name = 'restaurants_list.html'
    context_object_name = 'restaurants'


class CommentUpdate(PermissionMixin, FormView, SingleObjectMixin):

    form_class = CommentForm   # didn't use UpdateView because of CommentForm
    template_name = 'comment_update_form.html'

    model = Comment            # provide by SingleObjectMixin
    context_object_name = 'c'  # provide by SingleObjectMixin

    def get_success_url(self):
        self.object = self.get_object()
        return reverse('comment-view',
                       kwargs={'pk': self.object.restaurant.pk})

    def get_initial(self):
        initial = super(CommentUpdate, self).get_initial()

        comment = get_object_or_404(Comment, pk=self.kwargs.get('pk'))

        initial['visitor'] = comment.visitor
        initial['email'] = comment.email
        initial['content'] = comment.content

        return initial

    def form_valid(self, form):
        comment = get_object_or_404(Comment, pk=self.kwargs.get('pk'))

        c = Comment(
            id=self.kwargs.get('pk'),
            visitor=comment.visitor,
            email=form.cleaned_data['email'],
            content=form.cleaned_data['content'],
            date_time=timezone.localtime(timezone.now()),
            restaurant=comment.restaurant
        )
        c.save()

        c.userUpVotes.clear()    # reset votes due to edit comment
        c.userDownVotes.clear()  # reset votes due to edit comment

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super(CommentUpdate, self).get_context_data(
            object=self.object, **kwargs)

        return context


class CommentDelete(PermissionMixin, DeleteView):

    model = Comment

    def get_success_url(self):
        return reverse('comment-view',
                       kwargs={'pk': self.object.restaurant.pk})


class CommentView(FormView, SingleObjectMixin):

    form_class = CommentForm
    template_name = 'comments.html'

    model = Restaurant         # provide by SingleObjectMixin
    context_object_name = 'r'  # provide by SingleObjectMixin

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
            # M2M field operating after instance create
        )

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):  # overide context_object_name var
        self.object = self.get_object()
        context = super(CommentView, self).get_context_data(
            object=self.object, **kwargs)

        return context

    def get_object(self, queryset=None):
        obj = super(CommentView, self).get_object(queryset=queryset)
        comments = obj.comment_set.all()

        for c in comments:
            c.thisUserUpVote = c.userUpVotes.filter(
                id=self.request.user.id).count()
            c.thisUserDownVote = c.userDownVotes.filter(
                id=self.request.user.id).count()
            c.save()

        return obj


def vote(request):

    thread_id = int(request.POST.get('id'))
    vote_type = request.POST.get('type')
    vote_action = request.POST.get('action')

    thread = get_object_or_404(Comment, pk=thread_id)

    thisUserUpVote = thread.userUpVotes.filter(id=request.user.id).count()
    thisUserDownVote = thread.userDownVotes.filter(id=request.user.id).count()

    if (vote_action == 'vote'):
        if (thisUserUpVote == 0) and (thisUserDownVote == 0):
            if (vote_type == 'up'):
                thread.userUpVotes.add(request.user)
            elif (vote_type == 'down'):
                thread.userDownVotes.add(request.user)
            else:
                return HttpResponse('error-unknown vote type')
        else:
            return HttpResponse('error - already voted')
    elif (vote_action == 'recall-vote'):
        if (vote_type == 'up') and (thisUserUpVote == 1):
            thread.userUpVotes.remove(request.user)
        elif (vote_type == 'down') and (thisUserDownVote == 1):
            thread.userDownVotes.remove(request.user)
        else:
            return HttpResponse(
                'error - unknown vote type or no vote to recall')
    else:
        return HttpResponse('error - bad action')

    num_votes = thread.userUpVotes.count() - thread.userDownVotes.count()

    thisUserUpVote = thread.userUpVotes.filter(id=request.user.id).count()
    thisUserDownVote = thread.userDownVotes.filter(id=request.user.id).count()

    return HttpResponse(num_votes)


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
