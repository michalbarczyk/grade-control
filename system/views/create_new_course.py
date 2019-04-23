from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin


from system.models import Teacher, Course


class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    fields = ['title']

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = Teacher.objects.filter(user=self.request.user).first()
        return super().form_valid(form)