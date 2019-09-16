from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Journal
from django.views.generic import DetailView

# Add the following import
from django.http import HttpResponse

# Define the home view
def home(request):
  return HttpResponse('<h1>Welcome to Level Up Your Life!</h1>')

class JournalCreate(CreateView):
  model = Journal
  fields = ['title', 'author', 'about']
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class JournalUpdate(UpdateView):
  model = Journal
  fields = ['title', 'author', 'about']

class JournalDelete(DeleteView):
  model = Journal
  success_url = '/journals/'

def journals_index(request):
  journals = Journal.objects.all()
  return render(request, 'journals/index.html', { 'journals': journals })

def journals_detail(request, journal_id):
  journal = Journal.objects.get(id=journal_id)
  return render(request, 'journals/detail.html', {
    'journal': journal,
  })