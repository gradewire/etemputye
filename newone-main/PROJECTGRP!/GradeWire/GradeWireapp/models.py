from django.db import models

# Create your models here.

class Teacher(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField(unique=True)
    teacher_id=models.CharField(max_length=20)
    password=models.CharField(max_length=15)
    department=models.CharField(max_length=30)

from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=30)
    Class = models.CharField(max_length=20)
    department = models.CharField(max_length=30)
    register_id = models.CharField(max_length=20)
    mobile = models.CharField(max_length=10)  # Changed from IntegerField to CharField
    email = models.EmailField(unique=True)
    parent = models.CharField(max_length=30)
    parent_no = models.CharField(max_length=10)  # Changed from IntegerField to CharField
    password = models.CharField(max_length=15)
    
    def __str__(self):
        return self.name


