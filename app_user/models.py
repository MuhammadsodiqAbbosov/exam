from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class UserRoles(models.TextChoices):
    SuperAdmin = 'SuperAdmin', 'superAdmin'
    Admin = 'Admin', 'admin'
    Teacher = 'Teacher', 'teacher'
    Student = 'Student', 'student'

class CustomUser(AbstractUser):
    role = models.CharField(max_length=50, choices=UserRoles, default=UserRoles.Student)
    id_username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    gender = models.CharField(max_length=50)
    profile_image = models.ImageField(upload_to='profile_image/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id_username

class PostModel(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

    






User = get_user_model()