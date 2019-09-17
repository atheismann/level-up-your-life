from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3
from .models import Journal, Post, Task, Attachment
from .forms import SignupForm

S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'levelupyourlife-aplha'

# Define the home view
def home(request):
  return render(request, 'home.html')

class JournalList(ListView):
  model = Journal

class JournalDetail(DetailView):
  model = Journal
class JournalCreate(CreateView):
  model = Journal
  fields = ['title', 'about']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class JournalUpdate(UpdateView):
  model = Journal
  fields = ['title', 'about']

class JournalDelete(DeleteView):
  model = Journal
  success_url = '/journals/'

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
  return redirect('post_detail', post_id=post_id)

def assoc_post(request, journal_id, post_id):
  Journal.objects.get(id=journal_id).posts.add(post_id)
  return redirect('journal_detail', journal_id=journal_id)

def unassoc_post(request, journal_id, post_id):
  Journal.objects.get(id=journal_id).posts.remove(post_id)
  return redirect('journal_detail', journal_id=journal_id)

class PostList(ListView):
  model = Post

class PostDetail(DetailView):
  model = Post

class PostCreate(CreateView):
  model = Post
  fields = '__all__'

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class PostUpdate(UpdateView):
  model = Post
  fields = ['name', 'date', 'content', 'tasks', 'likes']

class PostDelete(DeleteView):
  model = Post
  success_url = '/posts/'

class TaskCreate(CreateView):
  model = Task
  fields = ['title', 'description', 'importance', 'progress']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class TaskUpdate(UpdateView):
  model = Task
  fields = ['title', 'description', 'importance', 'progress']

class TaskDelete(DeleteView):
  model = Task
  success_url = '/tasks/'

class TaskList(ListView):
  model = Task

class TaskDetail(DetailView):
  model = Task

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = SignupForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('journal_index')
    else:
      error_message = 'Invalid sign up - try again'
  form = SignupForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def assoc_assignedtasks(request, post_id, task_id):
  Post.objects.get(id=post_id).tasks.add(task_id)
  return redirect('post_detail', post_id=post_id)

def unassoc_assignedtasks(request, post_id, task_id):
  Post.objects.get(id=post_id).tasks.remove(task_id)
  return redirect('post_detail', post_id=post_id)
  
def assoc_completedtasks(request, post_id, task_id):
  Post.objects.get(id=post_id).tasks.add(task_id)
  return redirect('post_detail', post_id=post_id)

def unassoc_completedtasks(request, post_id, task_id):
  Post.objects.get(id=post_id).tasks.remove(task_id)
  return redirect('post_detail', post_id=post_id)
  
def assoc_inprogresstasks(request, post_id, task_id):
  Post.objects.get(id=post_id).tasks.add(task_id)
  return redirect('post_detail', post_id=post_id)

def unassoc_inprogresstasks(request, post_id, task_id):
  Post.objects.get(id=post_id).tasks.remove(task_id)
  return redirect('post_detail', post_id=post_id)
