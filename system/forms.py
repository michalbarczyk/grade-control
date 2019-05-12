from django import forms
from .models import Student, Course


class AddStudentForm(forms.Form):

    student = forms.ModelChoiceField(queryset=Student.objects.all())

"""
    def __init__(self, *args, **kwargs):

        course_pk = kwargs.pop('pk', None)
        print(course_pk)
        super(AddStudentForm, self).__init__(*args, **kwargs)
        #course = Course.objects.get(pk=course_pk)
        #all = Student.objects.all()
        #already_in_course = course.students.all()

        #self.fields['queryset'] = all.difference(already_in_course)
"""


class AddGradeForm(forms.Form):
    GRADES = (
        ('2.0', 'chlip'),
        ('3.0', 'ok'),
        ('4.0', 'dobre'),
        ('5.0', 'bardzodobre'),
    )

    student = forms.ModelChoiceField(queryset=Student.objects.all())
    grade = forms.ChoiceField(choices=GRADES)
"""
 def __init__(self, course):
        super(AddGradeForm, self).__init__()
        print('from log='+ course.title)
        #course = Course.objects.get(pk=course_pk)
"""







