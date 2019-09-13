from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('journal/create/', views.JournalCreate.as_view(), name='journal_create'),
]