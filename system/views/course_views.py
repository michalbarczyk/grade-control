from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView

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
        return super().form_valid(form)
        # obj.save()
        # return HttpResponseRedirect(reverse('teacher_courses'))


class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    # template_name = 'system/course_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # context['user'] = user
        context.update(append_sidebar(user))
        return context


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