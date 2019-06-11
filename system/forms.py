from django import forms
from .models import Student, Course, AcademicGrade, Event, ScoreGrade, PercentGrade
from django.core.validators import MinValueValidator, MaxValueValidator


class AddStudentForm(forms.Form):

    # queryset to be filled in constructor
    student = forms.ModelChoiceField(queryset=Student.objects.all())
"""
    def __init__(self, *args, **kwargs):

        course_pk = kwargs.pop('pk', None)
        super(AddStudentForm, self).__init__(*args, **kwargs)
        course = Course.objects.filter(pk=course_pk).first
        print(course)
        all_students = Student.objects.all()
        already_in_course = course.students.all()

        self.fields['student'].queryset = all_students.difference(already_in_course).all()
"""


class ManageAcademicGradeForm(forms.Form):
    NO_GRADE_STR = 'NO_GRADE'
    NONE_CHOICE = (NO_GRADE_STR, 'no grade')
    CHOICES = AcademicGrade.GRADES + (NONE_CHOICE,)

    def __init__(self, *args, **kwargs):

        course_pk = kwargs.pop('course_pk', None)
        event_pk = kwargs.pop('pk', None)

        super(ManageAcademicGradeForm, self).__init__(*args, **kwargs)
        course = Course.objects.filter(pk=course_pk).first()
        event = Event.objects.filter(pk=event_pk).first()
        for student in course.students.all():
            initial = get_current_academic_grade(event, student)
            self.fields[str(student.user.pk)] = forms.ChoiceField(choices=self.CHOICES,
                                                                  initial=initial,
                                                                  label=student.user.get_full_name)


def get_current_academic_grade(event, student):
    grade = AcademicGrade.objects.filter(event=event, owner=student).first()
    if grade is None:
        return ManageAcademicGradeForm.NO_GRADE_STR
    else:
        return grade.grade


class ManageScoreGradeForm(forms.Form):
    NO_GRADE_STR = 'NO_GRADE'
    NONE_CHOICE = (NO_GRADE_STR, 'no grade')

    def __init__(self, *args, **kwargs):

        course_pk = kwargs.pop('course_pk', None)
        event_pk = kwargs.pop('pk', None)

        super(ManageScoreGradeForm, self).__init__(*args, **kwargs)
        course = Course.objects.filter(pk=course_pk).first()
        event = Event.objects.filter(pk=event_pk).first()
        for student in course.students.all():
            initial = get_current_score_grade(event, student)
            self.fields[str(student.user.pk)] = forms.DecimalField(initial=initial,
                                                                   label=student.user.get_full_name, ##validators doesn't work
                                                                   validators=[MinValueValidator(0.00), MaxValueValidator(event.max_score)])


def get_current_score_grade(event, student):
    grade = ScoreGrade.objects.filter(event=event, owner=student).first()
    if grade is None:
        return ManageScoreGradeForm.NO_GRADE_STR
    else:
        return grade.grade


class ManagePercentGradeForm(forms.Form):
    NO_GRADE_STR = 'NO_GRADE'
    NONE_CHOICE = (NO_GRADE_STR, 'no grade')

    def __init__(self, *args, **kwargs):

        course_pk = kwargs.pop('course_pk', None)
        event_pk = kwargs.pop('pk', None)

        super(ManagePercentGradeForm, self).__init__(*args, **kwargs)
        course = Course.objects.filter(pk=course_pk).first()
        event = Event.objects.filter(pk=event_pk).first()
        for student in course.students.all():
            initial = get_current_percent_grade(event, student)
            self.fields[str(student.user.pk)] = forms.IntegerField(initial=initial, label=student.user.get_full_name)


def get_current_percent_grade(event, student):
    grade = PercentGrade.objects.filter(event=event, owner=student).first()
    if grade is None:
        return ManagePercentGradeForm.NO_GRADE_STR
    else:
        return grade.grade





