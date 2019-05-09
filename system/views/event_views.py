from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView

from system.models import Teacher, Course, Student, Event
from system.views import append_sidebar


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    fields = ['title', 'description']

    def get_context_data(self, *args, **kwargs):
        context = super(EventCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Add new event'
        context.update(append_sidebar(self.request.user))
        return context

    def form_valid(self, form):
        course = Course.objects.get(pk=self.kwargs['pk'])
        obj = form.save(commit=False)
        obj.course = course
        return super().form_valid(form)


"""
class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    # template_name = 'system/course_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # context['user'] = user
        context.update(append_sidebar(user))
        return context


class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    # template_name = 'system/course_list.html'
    context_object_name = 'courses'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = None

    def get_context_data(self, *args, **kwargs):
        context = super(CourseListView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Your courses'
        context.update(append_sidebar(self.request.user))
        return context

    def get_queryset(self):
        position = self.kwargs['position']
        # position = self.request.session['position']
        print(position)
        if position == 'teacher':
            user = Teacher.objects.filter(user=self.request.user).first()
            return Course.objects.filter(author=user)
        elif position == 'student':
            user = Student.objects.filter(user=self.request.user).first()
            return Course.objects.filter(students__user__username__contains=user)

"""




