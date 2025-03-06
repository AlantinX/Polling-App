from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Poll, Choice
from .forms import PollForm, ChoiceFormSet
from django.urls import reverse
from django.views.generic import DeleteView, ListView, DetailView, CreateView

class PollList(ListView):
    model = Poll
    template_name = 'polls/index.html'
    context_object_name = 'polls'
    
class Vote(DetailView):
    model = Poll
    template_name = 'polls/vote.html'
    context_object_name = 'poll'

    def post(self, request, *args, **kwargs):
        choice_id = request.POST.get('choice')
        choice = get_object_or_404(Choice, pk=choice_id)
        choice.votes += 1
        choice.save()
        return redirect('polls:index')

class NewPoll(CreateView):
    model = Poll
    form_class = PollForm
    template_name = 'polls/new_poll.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ChoiceFormSet(self.request.POST)
        else:
            context['formset'] = ChoiceFormSet()
        return context
    
    def form_valid(self, form):
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
    
  
# <--- Pages as functions in case I need them --->    
# 
# def index(request):
#     polls = Poll.objects.all()
#     return render(request, 'polls/index.html', {'polls': polls})

# def vote(request, poll_id):
#     poll = get_object_or_404(Poll, pk=poll_id)
#     if request.method == 'POST':
#         choice_id = request.POST.get('choice')
#         choice = get_object_or_404(Choice, pk=choice_id)
#         choice.votes += 1
#         choice.save()
#         return redirect('polls:index')
#     return render(request, 'polls/vote.html', {'poll': poll})

# def new_poll(request):
#     if request.method == 'POST':
#         form = PollForm(request.POST)
#         formset = ChoiceFormSet(request.POST)
#         if form.is_valid() and formset.is_valid():
#             poll = form.save()
#             choices = formset.save(commit=False)
#             for choice in choices:
#                 choice.poll = poll
#                 choice.save()
#             return redirect('polls:index')
#     else:
#         form = PollForm()
#         formset = ChoiceFormSet()
#     return render(request, 'polls/new_poll.html', {'form': form, 'formset': formset})