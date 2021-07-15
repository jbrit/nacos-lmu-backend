from django.contrib import admin
from .models import Course, PastQuestion, Semester, User

admin.site.register(User)
admin.site.register(Course)
admin.site.register(Semester)
admin.site.register(PastQuestion)