from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('user/', views.user_settings, name="user"),

  #planner paths
  path('planners/', views.PlannerList.as_view(), name='planner_index'),
  path('planners/create/', views.PlannerCreate.as_view(), name='planner_create'),
  path('planners/<int:pk>/', views.PlannerDetail.as_view(), name='planner_detail'),
  path('planners/<int:pk>/update/', views.PlannerUpdate.as_view(), name='planner_update'),
  path('planners/<int:pk>/delete/', views.PlannerDelete.as_view(), name='planner_delete'),
  path('planners/<int:planner_id>/assoc_entry/<int:entry_id>/', views.assoc_entry, name='assoc_entry'),
  path('planners/<int:planner_id>/unassoc_entry/<int:entry_id>/', views.unassoc_entry, name='unassoc_entry'),
  path('planners/<int:planner_id>/attachement/', views.add_attachment, name='add_attachment'),

  # entry paths
  path('entries/', views.EntryList.as_view(), name='entry_index'),
  path('entries/create/', views.EntryCreate.as_view(), name='entry_create'),
  path('entries/<int:pk>/', views.EntryDetail.as_view(), name='entry_detail'),
  path('entries/<int:pk>/update/', views.EntryUpdate.as_view(), name='entry_update'),
  path('entries/<int:pk>/delete/', views.EntryDelete.as_view(), name='entry_delete'),

  # Task Paths
  path('tasks/', views.TaskList.as_view(), name='task_index'),
  path('tasks/create/', views.TaskCreate.as_view(), name='task_create'),
  path('tasks/<int:pk>/', views.TaskDetail.as_view(), name='task_detail'),
  path('tasks/<int:pk>/update/', views.TaskUpdate.as_view(), name='task_update'),
  path('tasks/<int:pk>/delete/', views.TaskDelete.as_view(), name='task_delete'),

  #workout paths
  path('workouts/', views.WorkoutList.as_view(), name='workout_index'),
  path('workouts/create/', views.WorkoutCreate.as_view(), name='workout_create'),
  path('workouts/<int:pk>/', views.WorkoutDetail.as_view(), name='workout_detail'),
  path('workouts/<int:pk>/update/', views.WorkoutUpdate.as_view(), name='workout_update'),
  path('workouts/<int:pk>/delete/', views.WorkoutDelete.as_view(), name='workout_delete'),
  
  # mealplan paths
  path('mealplan/', views.MealPlanList.as_view(), name='mealplan_index'),
  path('mealplan/create/', views.MealPlanCreate.as_view(), name='mealplan_create'),
  path('mealplan/<int:pk>/', views.MealPlanDetail.as_view(), name='mealplan_detail'),
  path('mealplan/<int:pk>/update/', views.MealPlanUpdate.as_view(), name='mealplan_update'),
  path('mealplan/<int:pk>/delete/', views.MealPlanDelete.as_view(), name='mealplan_delete'),
  path('accounts/signup', views.signup, name='signup'),

  # entry assoc and unassoc
  path('entries/<int:entry_id>/assoc_mealplan/', views.assoc_mealplan, name='assoc_mealplan'),
  path('entries/<int:entry_id>/unassoc_mealplan/<int:mealplan_id>/', views.unassoc_mealplan, name='unassoc_mealplan'),
  path('entries/<int:entry_id>/assoc_assignedworkouts/', views.assoc_assignedworkouts, name='assoc_assignedworkouts'),
  path('entries/<int:entry_id>/unassoc_assignedworkouts/<int:assignedworkouts_id>/', views.unassoc_assignedworkouts, name='unassoc_assignedworkouts'),
  path('entries/<int:entry_id>/workout_complete/<int:workout_id>/', views.workout_complete, name='workout_complete'),
  path('entries/<int:entry_id>/unassoc_completedworkouts/<int:completedworkouts_id>/', views.unassoc_completedworkouts, name='unassoc_completedworkouts'),
  path('tasks/<int:entry_id>/task_complete/<int:task_id>/', views.task_complete, name='task_complete'),
  path('tasks/<int:entry_id>/unassoc_completedtasks/<int:completedtasks_id>/', views.unassoc_completedtasks, name='unassoc_completedtasks'),
  path('tasks/<int:entry_id>/assoc_assignedtasks/', views.assoc_assignedtasks, name='assoc_assignedtasks'),
  path('tasks/<int:entry_id>/unassoc_assignedtasks/<int:assignedtasks_id>/', views.unassoc_assignedtasks, name='unassoc_assignedtasks'),
]