from django.contrib import admin
from .models import user, type_task, task
# Register your models here.

admin.site.register(user)
admin.site.register(type_task)
admin.site.register(task)

