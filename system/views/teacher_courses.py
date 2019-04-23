from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from system.models import Teacher, Course
from system.views import append_sidebar


class TeacherCourseListView(LoginRequiredMixin, ListView):
    template_name = 'system/teacher_courses.html'
    context_object_name = 'teacher_courses'

    def get_context_data(self, *args, **kwargs):
        context = super(TeacherCourseListView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Your courses'
        context.update(append_sidebar(self.request.user))
        return context

    def get_queryset(self):
        teacher = Teacher.objects.filter(user=self.request.user).first()
        return Course.objects.filter(author=teacher)
