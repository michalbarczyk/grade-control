from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.user.username


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.user.username


class Course(models.Model):
    title = models.CharField(max_length=128)
    author = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('manage_groups')


class Event(models.Model):
    title = models.CharField(max_length=128)
    date = models.DateTimeField(default=timezone.now)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Grade(models.Model):
    owner = models.ForeignKey(Student, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    grade = models.CharField(max_length=4)

    def __str__(self):
        return self.grade



