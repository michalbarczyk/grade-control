from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin


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
        obj = form.save(commit=False)
        obj.author = Teacher.objects.filter(user=self.request.user).first()
        return super().form_valid(form)