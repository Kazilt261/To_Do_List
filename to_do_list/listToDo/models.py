from django.db import models

class user(models.Model):
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=150)
    hash_password_email = models.CharField(max_length=150)

class type_task(models.Model):
    type = models.CharField(max_length=50)

class task(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    end_date = models.DateField()
    type = models.ForeignKey(type_task, on_delete=models.CASCADE)
    user = models.ForeignKey(user, on_delete=models.CASCADE)