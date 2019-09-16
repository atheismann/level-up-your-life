from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3
from .models import Journal, Post, Task, Attachment


# Add the following import
from django.http import HttpResponse

S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'levelupyourlife-aplha'
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

def add_attachment(request, post_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
      s3 = boto3.client('s3')
      key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
      try:
          s3.upload_fileobj(photo_file, BUCKET, key)
          url = f"{S3_BASE_URL}{BUCKET}/{key}"
          photo = Attachment(url=url, post_id=post_id)
          photo.save()
      except:
          print('An error occurred uploading file to S3')
  return redirect('detail', post_id=post_id)

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

class TaskCreate(CreateView):
  model = Task
  fields = '__all__'

class TaskUpdate(UpdateView):
  model = Task
  fields = ['title', 'progress', 'author']

class TaskDelete(DeleteView):
  model = Task
  success_url = '/tasks/'

class TaskList(ListView):
  model = Task

class TaskDetail(DetailView):
  model = Task
