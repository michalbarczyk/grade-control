from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def home(request):
    context = {
        'title': 'home'
    }
    return render(request, 'system/home.html', context)
