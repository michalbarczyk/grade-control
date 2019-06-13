from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from system.views.overview import append_sidebar, student_exists, teacher_exists
from system.views import Course
from system.forms import AddStudentForm


def student_in_course(student, **kwargs):
    course = Course.objects.get(pk=kwargs['pk'])
    return course.students.filter(user=student.user).exists()


@login_required
def manage_students(request, **kwargs):
    course = Course.objects.get(pk=kwargs['pk'])
    if request.method == 'POST':

        form = AddStudentForm(request.POST)  # , **kwargs)

        if form.is_valid():

            student = form.cleaned_data['student']

            course.students.add(student)

    requesting = course.requesting.all()

    # then create new empty form
    user = request.user
    form = AddStudentForm()

    context = {
        'title': 'Add student to course',
        'form': form,
        'requesting': requesting,
        'course': course
    }

    context.update(append_sidebar(user))
    return render(request, 'system/manage_students.html', context)
