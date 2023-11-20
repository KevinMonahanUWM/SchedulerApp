from django.contrib import admin

from TAScheduler.models import User, TA, Course, Section, Instructor, Administrator, Lab, Lecture, TAToCourse, \
    InstructorToCourse

# Register your models here.
admin.site.register(User)
admin.site.register(TA)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(Instructor)
admin.site.register(Administrator)
admin.site.register(Lab)
admin.site.register(Lecture)
admin.site.register(TAToCourse)
admin.site.register(InstructorToCourse)
