from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from system.views.overview import append_sidebar
from system.views import Course, Event, Grade
from system.forms import AddGradeForm


@login_required
def manage_grades(request, **kwargs):

    if request.method == 'POST':

        form = AddGradeForm(request.POST, **kwargs)

        if form.is_valid():

            print('VALID')

            student = form.cleaned_data['student']
            grade_value = form.cleaned_data['grade']

            # DEBUG PRINT
            course = Course.objects.get(pk=kwargs['course_pk'])
            event = Event.objects.get(pk=kwargs['pk'])
            print(student.user.first_name)
            print(grade_value)



            grade = Grade()
            grade.grade = grade_value
            grade.owner = student
            grade.event = event
            grade.save()

    # then create new empty form
    user = request.user
    form = AddGradeForm(**kwargs)

    context = {
        'title': 'Add grade',
        'form': form
    }

    context.update(append_sidebar(user))
    return render(request, 'system/manage_grades.html', context)