from django.contrib import admin

from .models import Student , Teacher , Course, Event, Grade, Profile

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(Event)
admin.site.register(Grade)
admin.site.register(Profile)
