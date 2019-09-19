from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3
from .models import Planner, Entry, Task, Attachment, Workout, MealPlan, User
from .forms import SignupForm

S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'levelupyourlife-aplha'

# Define the home view
def home(request):
  return render(request, 'home.html')

def user_settings(request):
  User.objects.get(id=request.user.id).level_up()
  planners = Planner.objects.filter(user=request.user)
  return render(request, 'user.html', { 'planners': planners })

class MealPlanList(ListView):
  model = MealPlan

  def get_queryset(self):
    return MealPlan.objects.filter(user=self.request.user)

class MealPlanDetail(DetailView):
  model = MealPlan

class MealPlanCreate(CreateView):
  model = MealPlan
  fields = ['name', 'breakfast', 'lunch', 'dinner']

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

  def get_queryset(self):
    return Workout.objects.filter(user=self.request.user)

class WorkoutDetail(DetailView):
  model = Workout

class WorkoutCreate(CreateView):
  model = Workout
  fields = ['workout', 'description']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class WorkoutUpdate(UpdateView):
  model = Workout
  fields = ['workout', 'description']

class WorkoutDelete(DeleteView):
  model = Workout
  success_url = '/entries/entry_id/'

class PlannerList(ListView):
  model = Planner

  def get_queryset(self):
    return Planner.objects.filter(user=self.request.user)


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


class EntryList(ListView):
  model = Entry

  def get_queryset(self):
    return Entry.objects.filter(user=self.request.user)

class EntryDetail(DetailView):
  model = Entry

  def get_context_data(self, **kwargs):
    context = super(EntryDetail, self).get_context_data(**kwargs)
    context['workouts'] = Workout.objects.filter(user=self.request.user)
    context['mealplans'] = MealPlan.objects.filter(user=self.request.user)
    context['tasks'] = Task.objects.filter(user=self.request.user)
    return context

class EntryCreate(CreateView):
  model = Entry
  fields = ['date']
  
  def form_valid(self, form):
    planner = Planner.objects.first()
    form.instance.planner = planner
    form.instance.user = self.request.user
    form.instance.notes = ""
    return super().form_valid(form)

class EntryUpdate(UpdateView):
  model = Entry
  fields = ['date', 'notes']

class EntryDelete(DeleteView):
  model = Entry
  success_url = '/entries/'

class TaskCreate(CreateView):
  model = Task
  fields = ['title', 'description', 'importance', 'recurring']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

  def get_success_url(self):
    messages.success(self.request, 'Task Created')
    return redirect('planner_detail', planner_id=planner_id)

class TaskUpdate(UpdateView):
  model = Task
  fields = ['title', 'description', 'importance']

class TaskDelete(DeleteView):
  model = Task
  success_url = '/tasks/'

class TaskList(ListView):
  model = Task

  def get_queryset(self):
    return Task.objects.filter(user=self.request.user)

class TaskDetail(DetailView):
  model = Task

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
          photo = Attachment(url=url, pk=entry_id)
          photo.save()
      except:
          print('An error occurred uploading file to S3')
  return redirect('entry_detail', pk=entry_id)

def assoc_entry(request, planner_id, entry_id):
  Planner.objects.get(id=planner_id).entries.add(entry_id)
  return redirect('planner_detail', planner_id=planner_id)

def unassoc_entry(request, planner_id, entry_id):
  Planner.objects.get(id=planner_id).entries.remove(entry_id)
  return redirect('planner_detail', planner_id=planner_id)

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

def assoc_assignedtasks(request, entry_id):
  task_id = request.POST.get('task')
  Entry.objects.get(id=entry_id).assignedtasks.add(task_id)
  return redirect('entry_detail', pk=entry_id)

def unassoc_assignedtasks(request, entry_id, task_id):
  Entry.objects.get(id=entry_id).assignedtasks.remove(task_id)
  return redirect('entry_detail', pk=entry_id)
  
def task_complete(request, entry_id, task_id):
  Entry.objects.get(id=entry_id).assignedtasks.remove(task_id)
  Entry.objects.get(id=entry_id).completedtasks.add(task_id)
  task = Task.objects.get(id=task_id)
  user = User.objects.get(id=task.user.id)
  score = int(user.score) + int(task.importance)
  print(score)
  user.score = score
  user.save()
  user.level_up()
  return redirect('entry_detail', pk=entry_id)

def unassoc_completedtasks(request, entry_id, task_id):
  Entry.objects.get(id=entry_id).completedtasks.remove(task_id)
  return redirect('entry_detail', pk=entry_id)

###################################################################
def assoc_assignedworkouts(request, entry_id):
  workout_id = request.POST.get('workout')
  Entry.objects.get(id=entry_id).assignedworkouts.add(workout_id)
  return redirect('entry_detail', pk=entry_id)

def unassoc_assignedworkouts(request, entry_id, workout_id):
  Entry.objects.get(id=entry_id).assignedworkouts.remove(workout_id)
  return redirect('entry_detail', pk=entry_id)
  
def workout_complete(request, entry_id, workout_id):
  Entry.objects.get(id=entry_id).assignedworkouts.remove(workout_id)
  Entry.objects.get(id=entry_id).completedworkouts.add(workout_id)
  workout = Workout.objects.get(id=workout_id)
  user = User.objects.get(id=workout.user.id)
  score = int(user.score) + int(workout.importance)
  print(score)
  user.score = score
  user.save()
  user.level_up()
  return redirect('entry_detail', pk=entry_id)

def unassoc_completedworkouts(request, entry_id, workout_id):
  Entry.objects.get(id=entry_id).completedworkouts.remove(workout_id)
  return redirect('entry_detail', pk=entry_id)

###################################################################

def assoc_mealplan(request, entry_id):
  mealplan_id = request.POST.get('mealplan')
  Entry.objects.get(id=entry_id).mealplan.add(mealplan_id)
  return redirect('entry_detail', pk=entry_id)

def unassoc_mealplan(request, entry_id, mealplan_id):
  Entry.objects.get(id=entry_id).mealplan.remove(mealplan_id)
  return redirect('entry_detail', pk=entry_id)
  





