from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.forms.models import ModelForm
from django.forms.widgets import CheckboxSelectMultiple

from system.models import Student, Teacher
from system.views.overview import append_sidebar, student_exists, teacher_exists
from system.views import Course

"""
class CompanyForm(ModelForm):
    class Meta:
        model = Course
        fields = "course"

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)

        self.fields["course"].widget = CheckboxSelectMultiple()
        self.fields["course"].queryset = Student.objects.all()
"""


@login_required
def manage_students(request, **kwargs):
    user = request.user



    context = {
        'title': 'Manage students in course',
        'students': Student.objects.all(),
    }
    context.update(append_sidebar(user))
    return render(request, 'system/manage_students.html', context)


def change_teacher_status(request):
    user = request.user

    if teacher_exists(user):
        teacher = Teacher.objects.get(user=user)
        teacher.delete()
    else:
        teacher = Teacher(user=user)
        teacher.save()

    #return manage_groups(request)


def change_student_status(request):
    user = request.user

    if student_exists(user):
        student = Student.objects.get(user=user)
        student.delete()
    else:
        student = Student(user=user)
        student.save()

    #return manage_groups(request)
