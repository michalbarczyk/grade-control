from django import forms
from .models import Student, Course, Grade


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







class AddGradeForm(forms.Form):

    student = forms.ModelChoiceField(queryset=Student.objects.all())
    grade = forms.ChoiceField(choices=Grade.GRADES)

    def __init__(self, *args, **kwargs):

        course_pk = kwargs.pop('course_pk', None)
        event_pk = kwargs.pop('pk', None)
        super(AddGradeForm, self).__init__(*args, **kwargs)
        course = Course.objects.filter(pk=course_pk).first()

        self.fields['student'].queryset = course.students.all()













