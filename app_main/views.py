from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Post
posts = [
    {
        'author': 'CoreyMS',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'August 27, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'August 28, 2018'
    }
]

@login_required
def home(request):
    context = {
        'posts': Post.objects.all(),
        'title': 'homepage'
    }
    return render(request, 'app_main/home.html', context)


#def about(request):
#   return render(request, 'app_main/about.html', {'title': 'About'})

