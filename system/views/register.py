from django.contrib import messages
from django.shortcuts import render, redirect

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