from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.core.validators import MinValueValidator
import datetime


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.user.username

    def get_full_name(self):
        return self.user.first_name + ' ' + self.user.last_name


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.user.username


class Course(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=4000, blank=True)
    author = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('course-detail', kwargs={'pk': self.pk}) + '?position=teacher'


class Event(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=4000, blank=True)
    date = models.DateTimeField(default=datetime.datetime.now())
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    weight = models.IntegerField(default=1, validators=[MinValueValidator(1)])


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        kwargs ={'course_pk': self.course.pk, 'pk': self.pk}
        return reverse('event-detail', kwargs=kwargs) + '?position=teacher'


class Grade(models.Model):
    GRADES = (
        ('2.0', 'chlip'),
        ('3.0', 'ok'),
        ('3.5', 'ok +'),
        ('4.0', 'dobre'),
        ('4.5', 'dobre +'),
        ('5.0', 'bardzodobre'),
    )
    owner = models.ForeignKey(Student, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    grade = models.CharField(max_length=3, choices=GRADES)


    class Meta:
        unique_together = ('owner', 'event',)

    def __str__(self):
        return self.grade

"""
class ScoreGrade(models.Model):
    GRADES = (
        ('2.0', 'chlip'),
        ('3.0', 'ok'),
        ('3.5', 'ok +'),
        ('4.0', 'dobre'),
        ('4.5', 'dobre +'),
        ('5.0', 'bardzodobre'),
    )
    owner = models.ForeignKey(Student, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    grade = models.CharField(max_length=3, choices=GRADES)

    class Meta:
        unique_together = ('owner', 'event',)

    def __str__(self):
        return self.grade
"""

