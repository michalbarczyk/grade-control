from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def home(request):
    context = {
        'title': 'Home'
    }
    return render(request, 'system/home.html', context)
