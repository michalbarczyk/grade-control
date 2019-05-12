from django import forms
from .models import Student, Course

class AddStudentForm(forms.Form):

    student = forms.ModelChoiceField(queryset=Student.objects.all())

"""
    def __init__(self, *args, **kwargs):
        super(AddStudentForm, self).__init__(*args, **kwargs)
        course = Course.objects.get(pk=kwargs['pk'])
        all = Student.objects.all()
        already_in_course = course.students.all()

        self.fields['queryset'] = all.difference(already_in_course)
"""



