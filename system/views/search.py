from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from system.models import Course
from system.views import append_sidebar


@login_required
def search(request, **kwargs):
    q = request.GET.get('q', '')
    courses = None
    if q:
        courses = Course.objects.filter(title__icontains=q)
    context = {
        'title': 'Search',
        'courses': courses
    }
    user = request.user
    context.update(append_sidebar(user))
    return render(request, 'system/search.html', context)
