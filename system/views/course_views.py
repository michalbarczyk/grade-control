from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.shortcuts import render

from system.models import Teacher, Course, Student, AcademicGrade, Event
from system.views import append_sidebar


class CourseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
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

    def test_func(self):
        position = self.request.GET.get('position', '')
        if position == 'teacher':
            return Student.objects.filter(user=self.request.user).exists()
        return False


class CourseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Course
    # template_name = 'system/course_form.html'
    fields = ['title', 'description']

    def get_context_data(self, *args, **kwargs):
        context = super(CourseUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Update course'
        context.update(append_sidebar(self.request.user))
        return context

    def test_func(self):
        return test_author(self)


class CourseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Course
    success_url = '/overview/course_list?position=teacher'

    # template_name = 'system/course_confirm_delete.html'
    # fields = ['title', 'description']

    def get_context_data(self, *args, **kwargs):
        context = super(CourseDeleteView, self).get_context_data(*args, **kwargs)
        # context['title'] = 'Delete course'
        context.update(append_sidebar(self.request.user))
        return context

    def test_func(self):
        return test_author(self)


def test_author(classview):
    if classview.request.user == classview.get_object().author.user:
        return True
    return False


class CourseListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Course
    # template_name = 'system/course_list.html'
    context_object_name = 'courses'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = None

    def get_context_data(self, *args, **kwargs):
        context = super(CourseListView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Your courses'
        context['position'] = self.request.GET.get('position', '')
        context.update(append_sidebar(self.request.user))
        return context

    def get_queryset(self):
        position = self.request.GET.get('position', '')
        # position = self.request.session['position']
        print(position)
        if position == 'teacher':
            user = Teacher.objects.get(user=self.request.user)
            return Course.objects.filter(author=user)
        elif position == 'student':
            user = Student.objects.get(user=self.request.user)
            return Course.objects.filter(students__user__username=user)

    def test_func(self):
        position = self.request.GET.get('position', '')
        if position == 'teacher':
            return Teacher.objects.filter(user=self.request.user).exists()
        if position == 'student':
            return Student.objects.filter(user=self.request.user).exists()
        return False


class CourseDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Course
    context_object_name = 'course'

    # template_name = 'system/course_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # context['user'] = user
        position = self.request.GET.get('position', '')
        context['position'] = position

        course = Course.objects.get(pk=self.kwargs['pk'])
        course_events = Event.objects.filter(course=course)
        grade_summary = []
        for student in course.students.all():
            student_all_grades = AcademicGrade.objects.filter(owner=student)

            grades_str = ''
            for grade in student_all_grades:
                if grade.event in course_events:
                    grades_str = grades_str + str(grade.grade) + ' '

            grade_summary.append({'full_name': student.user.get_full_name, 'grades': grades_str})

        context['grade_summary'] = grade_summary
        context.update(append_sidebar(user))
        return context

    def test_func(self):
        position = self.request.GET.get('position', '')
        if position == 'teacher':
            return Course.objects.filter(author__user=self.request.user).exists()
        if position == 'student':
            return Student.objects.filter(user=self.request.user).exists()
        return False
