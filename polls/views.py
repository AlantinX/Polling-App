from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from .models import Poll, Choice, Vote
from .forms import PollForm, ChoiceFormSet, UserCreateForm
from django.urls import reverse
from django.views.generic import DeleteView, ListView, DetailView, CreateView, FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required


class Login(FormView):
    form_class = AuthenticationForm
    template_name = 'polls/login.html'

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('polls:index')


class Logout(LoginRequiredMixin, FormView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('polls:index')


class NewUser(FormView):
    form_class = UserCreateForm
    template_name = 'polls/register.html'
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_success_url(self):
        return reverse('polls:login')
    

class PollList(ListView):
    model = Poll
    template_name = 'polls/index.html'
    context_object_name = 'polls'
    
    
class PollDetail(DetailView):
    model = Poll
    template_name = 'polls/poll.html'
    context_object_name = 'poll'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['choices'] = self.object.choices.all()
        return context
    
    def post (self, request, *args, **kwargs):
        poll = self.get_object()
        choice_id = request.POST.get('choice')
        choice = poll.choices.get(pk=choice_id)
        if Vote.objects.filter(voter=request.user, choice__poll=poll).exists():
            return HttpResponseForbidden("You have already voted on this poll.")
        Vote.objects.create(choice=choice, voter=request.user)
        return redirect('polls:vote', pk=poll.pk)
    
    
class NewPoll(LoginRequiredMixin, CreateView):
    model = Poll
    form_class = PollForm
    template_name = 'polls/new_poll.html'
    login_url = 'polls:login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ChoiceFormSet(self.request.POST)
        else:
            context['formset'] = ChoiceFormSet()
        return context
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        context = self.get_context_data()
        formset = context['formset']
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect('polls:index')
        else:
            return self.render_to_response(self.get_context_data(form=form))
    
    def get_success_url(self):
        return reverse('polls:index')


class DeletePoll(DeleteView):
    model = Poll

    def get_success_url(self):
        return reverse('polls:index')