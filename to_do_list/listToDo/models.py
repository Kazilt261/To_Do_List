import os
from django.db import models
from cryptography.fernet import Fernet

from django.conf import settings

cipher_suite = Fernet(b'K4ukS6A4Ftj31Famj3raNx0zPTQILBfcgR4gBoi11qc=')

class user(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=150, unique=True)
    hash_password_email = models.CharField(max_length=150, unique=True)

class type_task(models.Model):
    type = models.CharField(max_length=50)
class task(models.Model):
    title = models.TextField()
    description = models.TextField()
    end_date = models.DateField()
    type = models.TextField()
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Encripta los campos antes de guardar
        if self.title:
            self.title = cipher_suite.encrypt(self.title.encode()).decode()

        if self.description:
            self.description = cipher_suite.encrypt(self.description.encode()).decode()

        # Guarda los datos encriptados en la base de datos
        super(task, self).save(*args, **kwargs)

    @classmethod
    def from_db(cls, db, field_names, values):
        # Recupera la instancia desde la base de datos y desencripta los campos
        instance = super().from_db(db, field_names, values)

        # Desencripta los campos después de que se hayan recuperado
        if instance.title:
            try:
                instance.title = cipher_suite.decrypt(instance.title.encode()).decode()
            except (ValueError, TypeError):
                pass  # Si no se puede desencriptar, lo dejamos encriptado

        if instance.description:
            try:
                instance.description = cipher_suite.decrypt(instance.description.encode()).decode()
            except (ValueError, TypeError):
                pass

        return instance