from django.contrib.auth.decorators import login_required
from django.shortcuts import render


from system.models import Teacher, Course


@login_required
def teacher_courses(request):
    teacher = Teacher.objects.filter(user=request.user).first()
    context = {
        'title': 'Teacher courses',
        'teacher_courses': Course.objects.filter(author=teacher).all()
    }
    return render(request, 'system/teacher_courses.html', context)


