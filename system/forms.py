from django import forms
from .models import Student, Course, Grade, Event



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
"""


class ManageGradesForm(forms.Form):
    NO_GRADE_STR = 'NO_GRADE'
    NONE_CHOICE = (NO_GRADE_STR, 'no grade')
    CHOICES = Grade.GRADES + (NONE_CHOICE,)

    def __init__(self, *args, **kwargs):

        print(self.CHOICES)

        course_pk = kwargs.pop('course_pk', None)
        event_pk = kwargs.pop('pk', None)

        super(ManageGradesForm, self).__init__(*args, **kwargs)
        course = Course.objects.filter(pk=course_pk).first()
        event = Event.objects.filter(pk=event_pk).first()
        for student in course.students.all():
            initial = get_current_grade(event, student)
            self.fields[str(student.user.pk)] = forms.ChoiceField(choices=self.CHOICES,
                                                                  initial=initial,
                                                                  label=student.get_full_name())


def get_current_grade(event, student):
    grade = Grade.objects.filter(event=event, owner=student).first()
    if grade is None:
        return ManageGradesForm.NO_GRADE_STR
    else:
        return grade.grade













