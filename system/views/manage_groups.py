from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from system.models import Grade, Student, Teacher
from system.views.overview import append_sidebar


@login_required
def manage_groups(request):
    user = request.user

    context = {
        'title': 'Manage your groups'
    }
    context.update(append_sidebar(user))
    return render(request, 'system/manage_groups.html', context)
