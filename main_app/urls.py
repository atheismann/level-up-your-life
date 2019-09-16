from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('journals/create/', views.journalsCreate.as_view(), name='journals_create'),
  path('journals/', views.games_index, name='index'),
  path('journals/<int:journal_id>/', views.journals_detail, name='detail'),
  path('journals/<int:pk>/update/', views.JournalUpdate.as_view(), name='journals_update'),
  path('journals/<int:pk>/delete/', views.JournalDelete.as_view(), name='journals_delete'),
]