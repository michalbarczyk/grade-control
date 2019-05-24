from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from system.views.overview import append_sidebar
from system.views import Course, Event, Grade, CourseDetailView
from system.forms import ManageGradesForm


@login_required
def manage_grades(request, **kwargs):

    if request.method == 'POST':

        form = ManageGradesForm(request.POST, **kwargs)

        if form.is_valid():
            print('FORM VALID')

            course = Course.objects.get(pk=kwargs['course_pk'])
            event = Event.objects.get(pk=kwargs['pk'])

            for student in course.students.all():
                db_grade = get_current_grade(event, student)
                form_grade_value = form.cleaned_data[str(student.user.pk)]

                if db_grade is None:
                    if form_grade_value != ManageGradesForm.NO_GRADE_STR:
                        print('#insert')
                        insert_grade(event, student, form_grade_value)
                else:
                    if form_grade_value == ManageGradesForm.NO_GRADE_STR:
                        print('#delete')
                        delete_grade(db_grade)
                    elif form_grade_value != db_grade.grade:
                        print('#update')
                        update_grade(db_grade, form_grade_value)

            return redirect(event)
        else:
            print('FORM INVALID')
    else:

        # then create new empty form
        user = request.user
        form = ManageGradesForm(**kwargs)

        context = {
            'title': 'Manage grades',
            'form': form
        }

        context.update(append_sidebar(user))
        return render(request, 'system/manage_grades.html', context)


def insert_grade(event, owner, new_grade_value):
    grade = Grade()
    grade.grade = new_grade_value
    grade.owner = owner
    grade.event = event
    grade.save()


def update_grade(old_grade, new_grade_value):
    owner = old_grade.owner
    event = old_grade.event

    old_grade.delete()

    grade = Grade()
    grade.grade = new_grade_value
    grade.owner = owner
    grade.event = event
    grade.save()


def delete_grade(grade):
    grade.delete()


def get_current_grade(event, student):
    return Grade.objects.filter(event=event, owner=student).first()



