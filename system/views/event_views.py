from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.models import User

from system.models import Teacher, Course, Student, Event, Grade
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


class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        course = Course.objects.get(pk=self.kwargs['course_pk'])
        event = Event.objects.get(pk=self.kwargs['pk'])

        grade_summary = []
        for student in course.students.all():
            print(student.user.first_name)
            event_grade = Grade.objects.filter(owner=student, event=event).first()
            print(event_grade)
            if event_grade is None:
                event_grade = 'no grade'
            grade_summary.append({'name': student.user.first_name + ' ' + student.user.last_name, 'grade': event_grade})

        context['grade_summary'] = grade_summary
        context.update(append_sidebar(user))
        return context


class EventListView(LoginRequiredMixin, ListView):
    model = Event
    context_object_name = 'events'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = None

    def get_context_data(self, *args, **kwargs):
        context = super(EventListView, self).get_context_data(*args, **kwargs)

        context['title'] = self.get_title
        context.update(append_sidebar(self.request.user))
        return context

    def get_queryset(self):
        course = Course.objects.get(pk=self.kwargs['pk'])
        return Event.objects.filter(course=course)

    def get_title(self):
        course = Course.objects.get(pk=self.kwargs['pk'])
        return 'Events in "' + course.title + '"'






