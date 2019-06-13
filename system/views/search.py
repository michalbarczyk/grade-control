from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from system.models import Course, Student
from system.views import append_sidebar


@login_required
def search(request):
    q = request.GET.get('q', '')
    courses = None
    own_courses = None
    requested_courses = None
    user = request.user
    if q:
        courses = Course.objects.filter(title__icontains=q)
        own_courses = courses.filter(students__user__username=user)
        requested_courses = courses.filter(requesting__user__username=user)
    leave_button = {'text': 'Leave', 'style': 'btn btn-danger btn-sm mt-1 mb-1'}
    requested_button = {'text': 'Cancel request', 'style': 'btn btn-info btn-sm mt-1 mb-1'}
    join_button = {'text': 'Enroll', 'style': 'btn btn-success btn-sm mt-1 mb-1'}

    is_student = Student.objects.filter(user=user).exists()

    context = {
        'is_student': is_student,
        'title': 'Search',
        'courses': courses,
        'own_courses': own_courses,
        'requested_courses': requested_courses,
        'leave_button': leave_button,
        'requested_button': requested_button,
        'join_button': join_button
    }
    context.update(append_sidebar(user))
    return render(request, 'system/search.html', context)


def update_requesting(request, pk):
    user = request.user
    course_pk = pk
    course = Course.objects.get(pk=course_pk)

    if request.method == 'POST':
        if course.students.filter(user=user).first():
            print('skasowano studenta')
            course.students.remove(course.students.filter(user=user).first())
        elif course.requesting.filter(user=user).first():
            print('skasowano request')
            course.requesting.remove(course.requesting.filter(user=user).first())
        else:
            print('dodano request')
            student = user.student
            course.requesting.add(student)

    return search(request)
