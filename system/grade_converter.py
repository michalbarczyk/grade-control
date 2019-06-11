from .models import AcademicGrade, ScoreGrade, PercentGrade, Event, Student, Course


def get_percentage_of_score(score_grade):
    max_score = score_grade.event.max_score
    return 100 * float(score_grade.grade)/float(max_score)


def score_to_academic(score_grade):
    percentage = get_percentage_of_score(score_grade)
    if percentage < 50.0:
        return '2.0'
    elif 60.0 > percentage >= 50.0:
        return '3.0'
    elif 70.0 > percentage >= 60.0:
        return '3.5'
    elif 80.0 > percentage >= 70.0:
        return '4.0'
    elif 90.0 > percentage >= 80.0:
        return '4.5'
    elif percentage >= 90.0:
        return '5.0'


def percent_to_academic(percent_grade):
    percentage = percent_grade.grade
    if percentage < 50.0:
        return '2.0'
    elif 60.0 > percentage >= 50.0:
        return '3.0'
    elif 70.0 > percentage >= 60.0:
        return '3.5'
    elif 80.0 > percentage >= 70.0:
        return '4.0'
    elif 90.0 > percentage >= 80.0:
        return '4.5'
    elif percentage >= 90.0:
        return '5.0'


def get_final_academic_grade(student, course):

    course_events = Event.objects.filter(course=course)
    student_academic_grades = AcademicGrade.objects.filter(owner=student)
    student_score_grades = ScoreGrade.objects.filter(owner=student)
    student_percent_grades = PercentGrade.objects.filter(owner=student)

    grade_sum = 0
    weight_sum = 0

    for grade in student_academic_grades:
        if grade.event in course_events:
            grade_sum += (float(grade.grade) * grade.event.weight)
            weight_sum += grade.event.weight

    for grade in student_score_grades:
        if grade.event in course_events:
            converted = score_to_academic(grade)
            grade_sum += (float(converted) * grade.event.weight)
            weight_sum += grade.event.weight

    for grade in student_percent_grades:
        if grade.event in course_events:
            converted = percent_to_academic(grade)
            grade_sum += (float(converted) * grade.event.weight)
            weight_sum += grade.event.weight

    if weight_sum == 0:
        return None

    return str(round(grade_sum / weight_sum, 2))







