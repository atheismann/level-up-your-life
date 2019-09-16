from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('journals/create/', views.JournalCreate.as_view(), name='journal_create'),
  path('journals/', views.journals_index, name='index'),
  path('journals/<int:journal_id>/', views.journals_detail, name='detail'),
  path('journals/<int:pk>/update/', views.JournalUpdate.as_view(), name='journal_update'),
  path('journals/<int:pk>/delete/', views.JournalDelete.as_view(), name='journal_delete'),
  path('journals/<int:journal_id>/assoc_post/<int:post_id>/', views.assoc_post, name='assoc_post'),
  path('journals/<int:journal_id>/unassoc_post/<int:post_id>/', views.unassoc_post, name='unassoc_post'),
  path('posts/', views.PostList.as_view(), name='post_index'),
  path('posts/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
  path('posts/create/', views.PostCreate.as_view(), name='post_create'),
  path('posts/<int:pk>/update/', views.PostUpdate.as_view(), name='post_update'),
  path('posts/<int:pk>/delete/', views.PostDelete.as_view(), name='post_delete'),
  path('tasks/', views.TaskList.as_view(), name='task_index'),
  path('tasks/<int:pk>/', views.TaskDetail.as_view(), name='task_detail'),
  path('tasks/create/', views.TaskCreate.as_view(), name='task_create'),
  path('tasks/<int:pk>/update/', views.TaskUpdate.as_view(), name='task_update'),
  path('tasks/<int:pk>/delete/', views.TaskDelete.as_view(), name='task_delete'),
]