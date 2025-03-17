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
    
class Student(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=18)
    grade = models.CharField(max_length=50) 

    

class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(Student, related_name="groups")

    def __str__(self):
        return self.name
    

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    groups = models.ManyToManyField(Group, related_name='teachers')

    def __str__(self):
        return self.name

class TeacherGroup(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.teacher.name} - {self.group.name}"
    

class Lesson(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    groups = models.ManyToManyField(Group, related_name='lessons')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='lessons')

    def __str__(self):
        return self.title


User = get_user_model()