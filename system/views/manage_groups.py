from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from system.models import Student, Teacher
from system.views.overview import append_sidebar, student_exists, teacher_exists


@login_required
def manage_groups(request):
    user = request.user
    leave_button = {'text': 'Leave', 'style': 'btn btn-danger'}
    join_button = {'text': 'Join', 'style': 'btn btn-success'}


    if student_exists(user):
        button_s = leave_button
    else:
        button_s = join_button

    if teacher_exists(user):
        button_t = leave_button
    else:
        button_t = join_button

    context = {
        'title': 'Manage your groups',
        'button_s': button_s,
        'button_t': button_t,
    }
    context.update(append_sidebar(user))
    return render(request, 'system/manage_groups.html', context)


def change_teacher_status(request):
    user = request.user

    if teacher_exists(user):
        teacher = Teacher.objects.get(user=user)
        teacher.delete()
    else:
        teacher = Teacher(user=user)
        teacher.save()

    return manage_groups(request)


def change_student_status(request):
    user = request.user

    if student_exists(user):
        student = Student.objects.get(user=user)
        student.delete()
    else:
        student = Student(user=user)
        student.save()

    return manage_groups(request)
