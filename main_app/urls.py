from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('journals/create/', views.JournalCreate.as_view(), name='journals_create'),
  path('journals/', views.journals_index, name='index'),
  path('journals/<int:journal_id>/', views.journals_detail, name='detail'),
  path('journals/<int:pk>/update/', views.JournalUpdate.as_view(), name='journals_update'),
  path('journals/<int:pk>/delete/', views.JournalDelete.as_view(), name='journals_delete'),
  path('journals/<int:journal_id>/assoc_post/<int:post_id>/', views.assoc_post, name='assoc_post'),
]