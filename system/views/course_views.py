from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.shortcuts import render

from system.models import Teacher, Course, Student, Grade, Event
from system.views import append_sidebar


class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    # template_name = 'system/course_form.html'
    fields = ['title', 'description']

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


class CourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Course
    # template_name = 'system/course_form.html'
    fields = ['title', 'description']

    def get_context_data(self, *args, **kwargs):
        context = super(CourseUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Update course'
        context.update(append_sidebar(self.request.user))
        return context


class CourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Course
    success_url = '/overview/course_list/teacher/'
    # template_name = 'system/course_confirm_delete.html'
    # fields = ['title', 'description']

    def get_context_data(self, *args, **kwargs):
        context = super(CourseDeleteView, self).get_context_data(*args, **kwargs)
        # context['title'] = 'Delete course'
        context.update(append_sidebar(self.request.user))
        return context

    def test_func(self):
        course = self.get_object()
        if self.request.user == course.author:
            return True
        return False


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


class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    context_object_name = 'course'
    # template_name = 'system/course_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # context['user'] = user

        course = Course.objects.get(pk=self.kwargs['pk'])
        course_events = Event.objects.filter(course=course)
        grade_summary = []
        for student in course.students.all():
            student_all_grades = Grade.objects.filter(owner=student)

            grades_str = ''
            for grade in student_all_grades:
                if grade.event in course_events:
                    grades_str = grades_str + str(grade.grade) + ' '

            grade_summary.append({'full_name': student.user.get_full_name, 'grades': grades_str})

        context['grade_summary'] = grade_summary
        context.update(append_sidebar(user))
        return context
