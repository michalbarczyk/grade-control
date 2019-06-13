from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from system.models import Teacher, Course, Student, AcademicGrade, Event, ScoreGrade, PercentGrade
from system.views import append_sidebar
from system.grade_converter import get_final_academic_grade


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
        if Teacher.objects.filter(user=self.request.user).exists():
            return True
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

        # naive usage of teacher course detail view for particular student
        #if position == 'student':
         #   students = Student.objects.filter(user=user)

        grade_summary = []

        if position == 'teacher':
            students = course.students.all()

            for student in students:
                student_academic_grades = AcademicGrade.objects.filter(owner=student)
                student_score_grades = ScoreGrade.objects.filter(owner=student)
                student_percent_grades = PercentGrade.objects.filter(owner=student)

                grades_str = ''
                for grade in student_academic_grades:
                    if grade.event in course_events:
                        grades_str = grades_str + str(grade.grade) + ' '

                for grade in student_score_grades:
                    if grade.event in course_events:
                        grades_str = grades_str + str(grade.grade) + '/' + str(grade.event.max_score) + ' '

                for grade in student_percent_grades:
                    if grade.event in course_events:
                        grades_str = grades_str + str(grade.grade) + '% '

                student_data = {'full_name': student.user.get_full_name,
                                'grades': grades_str,
                                }
                final_grade = get_final_academic_grade(student, course)
                if final_grade is not None:
                    student_data['final_grade'] = final_grade
                grade_summary.append(student_data)

        elif position == 'student':

            student = Student.objects.filter(user=user).first()

            student_academic_grades = AcademicGrade.objects.filter(owner=student)
            student_score_grades = ScoreGrade.objects.filter(owner=student)
            student_percent_grades = PercentGrade.objects.filter(owner=student)

            for grade in student_academic_grades:
                if grade.event in course_events:
                    grade_desc = {
                        'event': grade.event.title,
                        'grade': grade.grade
                    }

                    grade_summary.append(grade_desc)

            for grade in student_score_grades:
                if grade.event in course_events:
                    grade_desc = {
                        'event': grade.event.title,
                        'grade': str(grade.grade) + '/' + str(grade.event.max_score)
                    }

                    grade_summary.append(grade_desc)

            for grade in student_percent_grades:
                if grade.event in course_events:
                    grade_desc = {
                        'event': grade.event.title,
                        'grade': str(grade.grade) + '% '
                    }

                    grade_summary.append(grade_desc)

            final_grade = get_final_academic_grade(student, course)
            if final_grade is not None:
                context['final_grade'] = final_grade

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


def submit_request(request):
    pk = request.GET.get('pk')
    course = Course.objects.get(pk=pk)
    submitted = request.GET.get('s')
    username = request.GET.get('student')
    user = User.objects.get(username=username)
    print('xd')
    print(user.get_full_name)
    student = Student.objects.get(pk=user.student.pk)

    course.requesting.remove(student)
    if submitted == 'accept':
        course.students.add(student)

    return CourseDetailView.as_view()(request, pk=pk)
