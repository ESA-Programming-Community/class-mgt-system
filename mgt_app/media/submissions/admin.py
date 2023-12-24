from django.contrib import admin

from ceibs_app import models
from import_export.admin import ExportActionMixin


class RoleAdmin(admin.ModelAdmin):
    list_display = ['role', 'role_department']


class StudentDetailAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ['student_id', 'first_name', 'last_name', 'gender']


class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'program', 'department', 'student_class', 'intake_year', 'completion_year', 'active']


# Register your models here.
admin.site.register(models.Department)
admin.site.register(models.Program)
admin.site.register(models.RoleDepartment)
admin.site.register(models.Faculty)
admin.site.register(models.StudentClass)
admin.site.register(models.Role, RoleAdmin)
admin.site.register(models.AcademicDegree)
admin.site.register(models.StudentDetail, StudentDetailAdmin)
admin.site.register(models.Lecturer)
admin.site.register(models.Level)
admin.site.register(models.Staff)
admin.site.register(models.Enrollment, EnrollmentAdmin)








