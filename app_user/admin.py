from django.contrib import admin
from app_user.models import Teacher, Student, Group
from app_user.models import TeacherGroup

admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Group)


@admin.register(TeacherGroup)
class TeacherGroupAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'group')