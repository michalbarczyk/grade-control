from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime


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
    description = models.TextField(max_length=4000, blank=True)
    author = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('course-detail', kwargs={'pk': self.pk}) + '?position=teacher'


class Event(models.Model):
    GRADE_TYPES = (
        ('academic_grade', 'academic grade'),
        ('score_grade', 'score grade'),
        ('percent_grade', 'percent grade'),
    )

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=4000, blank=True)
    date = models.DateTimeField(default=datetime.datetime.now())
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    weight = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    grade_type = models.CharField(max_length=64, choices=GRADE_TYPES, default='academic_grade')
    max_score = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        kwargs ={'course_pk': self.course.pk, 'pk': self.pk}
        return reverse('event-detail', kwargs=kwargs) + '?position=teacher'

    def get_grade_model(self):
        if self.grade_type == 'academic_grade':
            return AcademicGrade
        elif self.grade_type == 'score_grade':
            return ScoreGrade
        elif self.grade_type == 'percent_grade':
            return PercentGrade
        else:
            return None


class AcademicGrade(models.Model):
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


class ScoreGrade(models.Model):

    def get_max_score(self):
        event = Event.objects.get(event=self.event)
        return event.max_score

    owner = models.ForeignKey(Student, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=6, decimal_places=2,
                                validators=[MinValueValidator(0.00)])

    class Meta:
        unique_together = ('owner', 'event',)

    def __str__(self):
        return str(self.grade)


class PercentGrade(models.Model):

    owner = models.ForeignKey(Student, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    grade = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        unique_together = ('owner', 'event',)

    def __str__(self):
        return str(self.grade)






