from django.contrib import admin
from . import models
# Register your models here.


class StudentQuizMarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'final_score', 'total_score_for_quiz', 'date_completed']


admin.site.register(models.CustomUser)
admin.site.register(models.Quiz)
admin.site.register(models.Community)
admin.site.register(models.Module)
admin.site.register(models.Question)
admin.site.register(models.Resource)
admin.site.register(models.StudentQuizMark, StudentQuizMarkAdmin)
admin.site.register(models.Program)
admin.site.register(models.Answer)
admin.site.register(models.StudentAnswer)
admin.site.register(models.Faculty)
admin.site.register(models.Lesson)
admin.site.register(models.Assignment)
admin.site.register(models.Submission)







