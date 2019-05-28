from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from system.views.overview import append_sidebar
from system.forms import ManageAcademicGradeForm, ManageScoreGradeForm, ManagePercentGradeForm
from system.models import Course, Event, AcademicGrade, ScoreGrade, PercentGrade


@login_required
def manage_grades(request, **kwargs):

    course = Course.objects.get(pk=kwargs['course_pk'])
    event = Event.objects.get(pk=kwargs['pk'])

    if request.method == 'POST':

        if event.grade_type == 'academic_grade':
            form = ManageAcademicGradeForm(request.POST, **kwargs)
        elif event.grade_type == 'score_grade':
            form = ManageScoreGradeForm(request.POST, **kwargs)
        elif event.grade_type == 'percent_grade':
            form = ManagePercentGradeForm(request.POST, **kwargs)

        if form.is_valid():
            print('FORM VALID')
            if event.grade_type == 'academic_grade':
                process_academic_grade_form(course, event, form)
            elif event.grade_type == 'score_grade':
                process_score_grade_form(course, event, form)
            elif event.grade_type == 'percent_grade':
                process_percent_grade_form(course, event, form)
        else:
            print('FORM INVALID')

        return redirect(event)
    else:
        user = request.user
        if event.grade_type == 'academic_grade':
            form = ManageAcademicGradeForm(**kwargs)
        elif event.grade_type == 'score_grade':
            form = ManageScoreGradeForm(**kwargs)
        elif event.grade_type == 'percent_grade':
            form = ManagePercentGradeForm(**kwargs)

        context = {
            'title': 'Manage grades',
            'form': form
        }

        context.update(append_sidebar(user))
        return render(request, 'system/manage_grades.html', context)


def process_academic_grade_form(course, event, form):

    for student in course.students.all():
        db_grade = get_current_academic_grade(event, student)
        form_grade_value = form.cleaned_data[str(student.user.pk)]

        if db_grade is None:
            if form_grade_value != ManageAcademicGradeForm.NO_GRADE_STR:
                print('#insert')
                insert_academic_grade(event, student, form_grade_value)
        else:
            if form_grade_value == ManageAcademicGradeForm.NO_GRADE_STR:
                print('#delete')
                delete_academic_grade(db_grade)
            elif form_grade_value != db_grade.grade:
                print('#update')
                update_academic_grade(db_grade, form_grade_value)


def insert_academic_grade(event, owner, new_grade_value):
    grade = AcademicGrade()
    grade.grade = new_grade_value
    grade.owner = owner
    grade.event = event
    grade.save()


def update_academic_grade(old_grade, new_grade_value):
    owner = old_grade.owner
    event = old_grade.event

    old_grade.delete()

    grade = AcademicGrade()
    grade.grade = new_grade_value
    grade.owner = owner
    grade.event = event
    grade.save()


def delete_academic_grade(grade):
    grade.delete()


def get_current_academic_grade(event, student):
    return AcademicGrade.objects.filter(event=event, owner=student).first()


def process_score_grade_form(course, event, form):

    for student in course.students.all():
        db_grade = get_current_score_grade(event, student)
        form_grade_value = form.cleaned_data[str(student.user.pk)]

        if db_grade is None:
            if form_grade_value != ManageScoreGradeForm.NO_GRADE_STR:
                print('#insert')
                insert_score_grade(event, student, form_grade_value)
        else:
            if form_grade_value == ManageScoreGradeForm.NO_GRADE_STR:
                print('#delete')
                delete_score_grade(db_grade)
            elif form_grade_value != db_grade.grade:
                print('#update')
                update_score_grade(db_grade, form_grade_value)


def insert_score_grade(event, owner, new_grade_value):
    grade = ScoreGrade()
    grade.grade = new_grade_value
    grade.owner = owner
    grade.event = event
    grade.save()


def update_score_grade(old_grade, new_grade_value):
    owner = old_grade.owner
    event = old_grade.event

    old_grade.delete()

    grade = ScoreGrade()
    grade.grade = new_grade_value
    grade.owner = owner
    grade.event = event
    grade.save()


def delete_score_grade(grade):
    grade.delete()


def get_current_score_grade(event, student):
    return ScoreGrade.objects.filter(event=event, owner=student).first()


def process_percent_grade_form(course, event, form):

    for student in course.students.all():
        db_grade = get_current_percent_grade(event, student)
        form_grade_value = form.cleaned_data[str(student.user.pk)]

        if db_grade is None:
            if form_grade_value != ManagePercentGradeForm.NO_GRADE_STR:
                print('#insert')
                insert_percent_grade(event, student, form_grade_value)
        else:
            if form_grade_value == ManagePercentGradeForm.NO_GRADE_STR:
                print('#delete')
                delete_percent_grade(db_grade)
            elif form_grade_value != db_grade.grade:
                print('#update')
                update_percent_grade(db_grade, form_grade_value)


def insert_percent_grade(event, owner, new_grade_value):
    grade = PercentGrade()
    grade.grade = new_grade_value
    grade.owner = owner
    grade.event = event
    grade.save()


def update_percent_grade(old_grade, new_grade_value):
    owner = old_grade.owner
    event = old_grade.event

    old_grade.delete()

    grade = PercentGrade()
    grade.grade = new_grade_value
    grade.owner = owner
    grade.event = event
    grade.save()


def delete_percent_grade(grade):
    grade.delete()


def get_current_percent_grade(event, student):
    return PercentGrade.objects.filter(event=event, owner=student).first()



