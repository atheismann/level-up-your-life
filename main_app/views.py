from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3
from .models import Planner, Entry, Task, Attachment, Workout, MealPlan
from .forms import SignupForm

S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'levelupyourlife-aplha'

# Define the home view
def home(request):
  return render(request, 'home.html')

class MealPlanList(ListView):
  model = MealPlan

class MealPlanDetail(DetailView):
  model = MealPlan

class MealPlanCreate(CreateView):
  model = MealPlan
  fields = '__all__'

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class MealPlanUpdate(UpdateView):
  model = MealPlan
  fields = ['breakfast', 'lunch', 'dinner']

class MealPlanDelete(DeleteView):
  model = MealPlan
  success_url = '/entries/entry_id/'

class WorkoutList(ListView):
  model = Workout

class WorkoutDetail(DetailView):
  model = Workout

class WorkoutCreate(CreateView):
  model = Workout
  fields = '__all__'

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class WorkoutUpdate(UpdateView):
  model = Workout
  fields = ['workoutType']

class WorkoutDelete(DeleteView):
  model = Workout
  success_url = '/entries/entry_id/'

class PlannerList(ListView):
  model = Planner

class PlannerDetail(DetailView):
  model = Planner
class PlannerCreate(CreateView):
  model = Planner
  fields = ['title', 'about']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class PlannerUpdate(UpdateView):
  model = Planner
  fields = ['title', 'about']

class PlannerDelete(DeleteView):
  model = Planner
  success_url = '/planners/'

def about(request):
  return render(request, 'about.html')

def add_attachment(request, entry_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
      s3 = boto3.client('s3')
      key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
      try:
          s3.upload_fileobj(photo_file, BUCKET, key)
          url = f"{S3_BASE_URL}{BUCKET}/{key}"
          photo = Attachment(url=url, entry_id=entry_id)
          photo.save()
      except:
          print('An error occurred uploading file to S3')
  return redirect('entry_detail', entry_id=entry_id)

def assoc_entry(request, planner_id, entry_id):
  Planner.objects.get(id=planner_id).entries.add(entry_id)
  return redirect('planner_detail', planner_id=planner_id)

def unassoc_entry(request, planner_id, entry_id):
  Planner.objects.get(id=planner_id).entries.remove(entry_id)
  return redirect('planner_detail', planner_id=planner_id)

class EntryList(ListView):
  model = Entry

class EntryDetail(DetailView):
  model = Entry

class EntryCreate(CreateView):
  model = Entry
  fields = ['date', 'planner']

class EntryUpdate(UpdateView):
  model = Entry
  fields = ['name', 'planner']

class EntryDelete(DeleteView):
  model = Entry
  success_url = '/entries/'

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
      return redirect('planner_index')
    else:
      error_message = 'Invalid sign up - try again'
  form = SignupForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def assoc_assignedtasks(request, entry_id, task_id):
  Entry.objects.get(id=entry_id).tasks.add(task_id)
  return redirect('entry_detail', entry_id=entry_id)

def unassoc_assignedtasks(request, entry_id, task_id):
  Entry.objects.get(id=entry_id).tasks.remove(task_id)
  return redirect('entry_detail', entry_id=entry_id)
  
def assoc_completedtasks(request, entry_id, task_id):
  Entry.objects.get(id=entry_id).tasks.add(task_id)
  return redirect('entry_detail', entry_id=entry_id)

def unassoc_completedtasks(request, entry_id, task_id):
  Entry.objects.get(id=entry_id).tasks.remove(task_id)
  return redirect('entry_detail', entry_id=entry_id)

###################################################################
def assoc_assignedworkout(request, entry_id, workout_id):
  Workout.objects.get(id=entry_id).workouts.add(workout_id)
  return redirect('entry_detail', entry_id=entry_id)

def unassoc_assignedworkout(request, entry_id, workout_id):
  Workout.objects.get(id=entry_id).workouts.remove(workout_id)
  return redirect('entry_detail', entry_id=entry_id)
  
def assoc_completedworkout(request, entry_id, workout_id):
  Workout.objects.get(id=entry_id).workouts.add(workout_id)
  return redirect('entry_detail', entry_id=entry_id)

def unassoc_completedworkout(request, entry_id, workout_id):
  Workout.objects.get(id=entry_id).workouts.remove(workout_id)
  return redirect('entry_detail', entry_id=entry_id)

###################################################################

def assoc_mealplan(request, entry_id, mealplan_id):
  MealPlan.objects.get(id=entry_id).workouts.add(mealplan_id)
  return redirect('entry_detail', entry_id=entry_id)

def unassoc_mealplan(request, entry_id, mealplan_id):
  MealPlan.objects.get(id=entry_id).workouts.remove(mealplan_id)
  return redirect('entry_detail', entry_id=entry_id)
  





