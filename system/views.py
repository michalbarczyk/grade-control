from django.shortcuts import render,  redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from system.models import Grade
from .forms import UserRegisterForm

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
def profile(request):
    return render(request, 'system/profile.html')


@login_required
def home(request):
    context = {
        'grades': Grade.objects.all(),
        'title': 'gradepage'
    }
    return render(request, 'system/home.html', context)