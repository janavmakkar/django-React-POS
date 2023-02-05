from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Permission(models.Model):
    name=models.CharField(max_length=200)

class Role(models.Model):
    name=models.CharField(max_length=200)
    permissions=models.ManyToManyField(Permission)


class User(AbstractUser):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.CharField(max_length=200, unique=True)
    role=models.ForeignKey(Role,on_delete=models.SET_NULL,null=True)
    password=models.CharField(max_length=200)
    username=None

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
