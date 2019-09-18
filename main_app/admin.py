from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Planner, Task, Entry

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Planner)
admin.site.register(Task)
admin.site.register(Entry)
