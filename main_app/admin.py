from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Journal, Task, Post

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Journal)
admin.site.register(Task)
admin.site.register(Post)
