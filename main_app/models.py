from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from datetime import date


IMPORTANCE = (
    ('1', 'Low Importance'),
    ('3', 'Medium Importance'),
    ('5', 'High Importance')
)

DAYS = (
    ('1', 'Monday'),
    ('2', 'Tuesday'),
    ('3', 'Wednesday'),
    ('4', 'Thursday'),
    ('5', 'Friday'),
    ('6', 'Saturday'),
    ('7', 'Sunday'),
)

class User(AbstractUser):
  pass
  score = models.IntegerField(default=0)
  level = models.CharField(max_length=100, default='Peasant')

  def level_up(self):
    if self.score <= 150:
      self.level = 'Peasant'
    elif self.score <= 300:
      self.level = 'Artisan'
    elif self.score <= 450:
      self.level = 'Ronan'
    elif self.score == 600:
      self.level = 'Samurai'
    elif self.score == 750:
      self.level = 'Daimyo'
    elif self.score == 1000:
      self.level = 'Shogun'
    else:
      self.level = 'Emperor'
    self.save()
    
class Workout(models.Model):
  workout = models.CharField(max_length=250)
  description = models.TextField(max_length=2500)
  importance = models.CharField(
    max_length=1,
    choices=IMPORTANCE,
    default=IMPORTANCE[1][0],
  )
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def get_absolute_url(self):
    return reverse('workout_detail', kwargs={'pk': self.id})

class MealPlan(models.Model):
  name = models.CharField(max_length=50)
  breakfast = models.CharField(max_length=50)
  lunch = models.CharField(max_length=50)
  dinner = models.CharField(max_length=50)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def get_absolute_url(self):
    return reverse('mealplan_detail', kwargs={'pk': self.id})

class Planner(models.Model):
  title = models.CharField(max_length=250)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  about = models.TextField(max_length=2500)

  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse('planner_detail', kwargs={'pk': self.id}) 

class Task(models.Model):
  title = models.CharField(max_length=100)
  description = models.TextField(max_length=2500)
  importance = models.CharField(
    max_length=1,
    choices=IMPORTANCE,
    default=IMPORTANCE[1][0],
  )
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def get_absolute_url(self):
    return reverse('task_detail', kwargs={'pk': self.id}) 
  
  def __str__(self):
    return f"{self.get_progress_display()} on {self.title}"
  
  def __str__(self):
    return f"{self.get_importance_display()} on {self.title}"

class Entry(models.Model):
  date = models.DateField(default=date.today)
  mealplan = models.ManyToManyField(MealPlan)
  planner = models.ForeignKey(Planner, on_delete=models.CASCADE)
  assignedtasks = models.ManyToManyField(Task, related_name="assignedTasks")
  completedtasks = models.ManyToManyField(Task, related_name="completedTasks")
  assignedworkouts = models.ManyToManyField(Workout, related_name="assignedWorkout")
  completedworkouts = models.ManyToManyField(Workout,   related_name="completedWorkout")
  notes = models.TextField(max_length=2500)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  
  def get_absolute_url(self):
    return reverse('entry_detail', kwargs={'pk': self.id}) 

  def get_week_number(self):
    return self.date.isocalendar()[1]
  
  def get_day_of_week(self):
    d = self.date.isocalendar()[2]
    return DAYS[d-1][1]
  
  def current_week(self):
    return date.today().isocalendar()[1]

class Attachment(models.Model):
    url = models.CharField(max_length=200)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)

    def __str__(self):
        return f"Attachment for entry_id: {self.entry_id} @{self.url}"