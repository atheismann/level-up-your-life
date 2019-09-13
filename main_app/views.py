from django.shortcuts import render
from django.views.generic.edit import CreateView,
from .models import Journal

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