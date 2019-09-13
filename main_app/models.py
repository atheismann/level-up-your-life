from django.db import models
from django.urls import reverse
from .models import User


# Create your models here.

AUTHOR = (
    ('A', 'Andrew'),
    ('D', 'Daniel'),
    ('J', 'Joseph'),
)

class Journal(models.Model):
    title = models.CharField(max_length=250)
    author = models.CharField(max_length=250)
    about = models.TextField(max_length=250)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'journal_id': self.id})


class Author(models.Model):
  author = models.CharField(
    max_length=1,
    choices=AUTHOR,
    default=AUTHOR[0][0]
  )
  journal = models.ForeignKey(Journal, on_delete=models.CASCADE)

  def __str__(self):
    return "{self.get_session_display()} on {self.date}"

 