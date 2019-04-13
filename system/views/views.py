from django.shortcuts import render,  redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from system.models import Grade, Student
from system.forms import UserRegisterForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account has been created')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'system/register.html', {'form': form})

@login_required
def home(request):
    context = {
        'title': 'home'
    }
    return render(request, 'system/home.html', context)

@login_required
def overview(request):
    user = request.user
    student_exists = Student.objects.filter(user=user.id).exists()
    groups = []
    if student_exists:
        grades = Grade.objects.filter(owner_id=user.id)
        groups += 'Student'
    else:
        grades = None
    context = {
        'sidebar': True,
        'groups': groups,
        'grades': grades,
        #'grades': request.user.grade_set.all(),
        'title': 'overview'
    }
    return render(request, 'system/overview.html', context)

@login_required
def profile(request):
    context = {
        'title': 'profile'
    }
    return render(request, 'system/profile.html', context)