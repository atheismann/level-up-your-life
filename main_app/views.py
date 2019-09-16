from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3
from .models import Journal, Post, Task


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

def about(request):
  return render(request, 'about.html')

def assoc_post(request, journal_id, post_id):
  Journal.objects.get(id=journal_id).posts.add(post_id)
  return redirect('detail', journal_id=journal_id)

def unassoc_post(request, journal_id, post_id):
  Journal.objects.get(id=journal_id).posts.remove(post_id)
  return redirect('detail', journal_id=journal_id)

class PostList(ListView):
  model = Post

class PostDetail(DetailView):
  model = Post

class PostCreate(LoginRequiredMixin, CreateView):
  model = Post
  fields = '__all__'

class PostUpdate(UpdateView):
  model = Post
  fields = ['name', 'date', 'content', 'tasks', 'likes']

class PostDelete(DeleteView):
  model = Post
  success_url = '/posts/'