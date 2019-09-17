from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from datetime import date


IMPORTANCE = (
    ('1', 'Low Importance'),
    ('3', 'Medium Importance'),
    ('5', 'High Importance')
)


class User(AbstractUser):
  pass
  score = models.IntegerField(default=0)
  level = models.CharField(max_length=100, default='Newbie')

class Journal(models.Model):
  title = models.CharField(max_length=250)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  about = models.TextField(max_length=2500)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('journal_detail', kwargs={'pk': self.id}) 

class Task(models.Model):
  title = models.CharField(max_length=100)
  description = models.TextField(max_length=2500)
  importance = models.CharField(
    max_length=1,
    choices=IMPORTANCE,
    default=IMPORTANCE[0][1],
  )
  
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def get_absolute_url(self):
    return reverse('task_detail', kwargs={'pk': self.id}) 
  
  def __str__(self):
    return f"{self.get_progress_display()} on {self.title}"

class Post(models.Model):
  name = models.CharField(max_length=250)
  date = models.DateField(default=date.today)
  content = models.TextField(max_length=2500)
  journal = models.ForeignKey(Journal, on_delete=models.CASCADE)
  assignedtasks = models.ManyToManyField(Task, related_name="assignedTasks")
  completedtasks = models.ManyToManyField(Task, related_name="completedTasks")
  inprogresstasks = models.ManyToManyField(Task, related_name="inProgressTasks")

class Attachment(models.Model):
    url = models.CharField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"Attachment for post_id: {self.post_id} @{self.url}"