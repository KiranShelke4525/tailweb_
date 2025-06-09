from django.db import models

class Teacher(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=150)

class Student(models.Model):
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=100)
    marks = models.PositiveIntegerField()

    class Meta:
        unique_together = ('name', 'subject')
