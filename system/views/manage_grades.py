from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from system.views.overview import append_sidebar, student_exists, teacher_exists
from system.views import Course
from system.forms import AddGradeForm


@login_required
def manage_grades(request, **kwargs):

    if request.method == 'POST':

        form = AddGradeForm(request.POST)

        if form.is_valid():

            student = form.cleaned_data['student']
            course = Course.objects.get(pk=kwargs['pk'])
            # add pair course-student to DB
            course.students.add(student)

    # then create new empty form
    user = request.user
    form = AddGradeForm()

    context = {
        'title': 'Add grade',
        'form': form
    }

    context.update(append_sidebar(user))
    return render(request, 'system/manage_grades.html', context)