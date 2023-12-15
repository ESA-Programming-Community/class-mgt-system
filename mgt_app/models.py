from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class Faculty(models.Model):
    name = models.CharField(max_length=250, null=False, blank=False)
    faculty_head = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class Program(models.Model):
    faculty = models.ForeignKey(Faculty, null=False, blank=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=200, blank=False, null=False)
    last_name = models.CharField(max_length=200, blank=False, null=False)
    username = models.CharField(max_length=200, null=False, blank=False, unique=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, null=True, blank=True)
    approved = models.BooleanField(default=False)
    roles = (
        ("Student", "Student"),
        ("Instructor", "Instructor"),
        ("Co-Instructor", "Co-Instructor"),
        ("Admin", "Admin")
    )
    role = models.CharField(max_length=200, null=True, blank=True, choices=roles, default="Student")
    phone_number = models.PositiveBigIntegerField(blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    password1 = models.CharField(max_length=100, null=False, blank=False)
    password2 = models.CharField(max_length=100, null=False, blank=False)
    status_choices = (
        ("Active", "Active"),
        ("Inactive", "Inactive")
    )
    status = models.CharField(max_length=100, null=False, blank=False, default="Inactive", choices=status_choices)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.username}"



class Community(models.Model):
    name = models.CharField(max_length=250, null=False, blank=False)
    description = models.TextField(max_length=500, null=True, blank=True)
    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name="main_instructor")
    co_instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name="assistant_instructor")
    group_link = models.URLField(null=True, blank=True)
    members = models.ManyToManyField(CustomUser, null=True, blank=True)

    def __str__(self):
        return self.name



class Module(models.Model):
    module_number = models.PositiveIntegerField(null=False, blank=False)
    name = models.CharField(max_length=250, null=False, blank=False)
    description = models.TextField(max_length=500, null=True, blank=True)
    community_it_belongs_to = models.ForeignKey(Community, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    lesson_number = models.PositiveIntegerField(null=False, blank=False)
    title = models.CharField(max_length=250, null=False, blank=False)
    description = models.TextField(max_length=400, null=True, blank=True)
    link = models.URLField(blank=True, null=True)
    module_it_belongs_to = models.ForeignKey(Module, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class Resource(models.Model):
    title = models.CharField(max_length=250, null=False, blank=False)
    description = models.TextField(max_length=400, null=True, blank=True)
    link = models.URLField(blank=True, null=True)
    lesson_it_belongs_to = models.ForeignKey(Lesson, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Quiz(models.Model):
    quiz_number = models.PositiveIntegerField(auto_created=True)
    title = models.CharField(max_length=250, null=False, blank=False)
    description = models.TextField(max_length=400, null=True, blank=True)
    community_it_belongs_to = models.ForeignKey(Community, on_delete=models.CASCADE)
    choices = (
        ("Active", "Active"),
        ("Dead", "Dead")
    )
    status = models.CharField(max_length=200, null=False, blank=False, choices=choices, db_default="Dead")
    date_posted = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title


class Question(models.Model):
    question_number = models.PositiveIntegerField(null=False, blank=False)
    question_text = models.TextField(max_length=250, null=False, blank=False)
    # option1 = models.CharField(max_length=200, null=False, blank=False)
    # option2 = models.CharField(max_length=200, null=False, blank=False)
    # option3 = models.CharField(max_length=200, null=True, blank=True)
    # option4 = models.CharField(max_length=200, null=True, blank=True)
    # choices = (
    #     ("option1", "option1"),
    #     ("option2", "option2"),
    #     ("option3", "option3"),
    #     ("option4", "option4")
    # )
    # answer = models.CharField(max_length=200, null=False, blank=False, choices=choices)
    quiz_it_belongs_to = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return f"{self.question_number}. {self.question_text}"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=256, null=False, blank=False)
    is_correct = models.BooleanField(db_default=False)

    def __str__(self):
        return self.answer_text



class StudentAnswer(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    chosen_answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return self.chosen_answer.answer_text


class StudentQuizMark(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    final_score = models.CharField(max_length=200, null=True, blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    attempted = models.BooleanField()
    date_completed = models.DateTimeField()
    total_score_for_quiz = models.PositiveIntegerField(null=False, blank=False)

    def __str__(self):
        return f"{self.user} - {self.quiz.title} - {self.final_score}"


class Assignment(models.Model):
    assignment_number = models.PositiveBigIntegerField(null=False, blank=False)
    user_posted = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    assignment_title = models.CharField(max_length=250, null=False, blank=False)
    assignment_instruction = models.TextField(null=False, blank=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(db_default=False)
    community_it_belongs_to = models.ForeignKey(Community, on_delete=models.CASCADE)
    module_it_belongs_to = models.ForeignKey(Module, on_delete=models.CASCADE, null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.assignment_title

























