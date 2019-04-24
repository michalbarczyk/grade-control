from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView

from system.models import Teacher, Course
from system.views import append_sidebar


class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    fields = ['title']

    def get_context_data(self, *args, **kwargs):
        context = super(CourseCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Create new course'
        context.update(append_sidebar(self.request.user))
        return context

    def form_valid(self, form):
        teacher = Teacher.objects.filter(user=self.request.user).first()
        obj = form.save(commit=False)
        obj.author = teacher
        obj.save()
        # return super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('teacher_courses')
