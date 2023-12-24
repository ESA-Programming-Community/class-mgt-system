import datetime

import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from mgt_app import models, forms


def quiz_page(request, community_name):
    user = models.CustomUser.objects.get(id=request.user.id)
    community = models.Community.objects.get(name=community_name)
    name = community.name
    quizzes = models.Quiz.objects.filter(community_it_belongs_to=community, status="Active")
    student_quizzes = models.StudentQuizMark.objects.filter(user=user, quiz__community_it_belongs_to=community)
    modules = models.Module.objects.filter(community_it_belongs_to=community)
    quiz_data = []
    for quiz in quizzes:
        attempted = models.StudentQuizMark.objects.filter(user=user, quiz=quiz, quiz__community_it_belongs_to=community).exists()
        quiz_data.append((quiz, attempted))
    context = {
        'quizzes': quizzes,
        'community_name': name,
        'name': name,
        'student_quizzes': student_quizzes,
        'quiz_data': quiz_data,
        'modules': modules
    }
    messages.info(request, "NB: Once you click on attempt quiz, you will have to finish it. If for some reasons you did not finish it or you navigate off the page, the quiz will be rendered null and you will not be permitted to attempt it again.")
    return render(request, "layouts/quiz/quizzes.html", context=context)


def quiz_detail(request, community_name, quiz_title):
    community = models.Community.objects.get(name=community_name)
    quiz = models.Quiz.objects.get(title=quiz_title, community_it_belongs_to=community)
    questions = models.Question.objects.filter(quiz_it_belongs_to=quiz).order_by('question_number')
    answers = models.Answer.objects.filter(question__in=questions)
    modules = models.Module.objects.filter(community_it_belongs_to=community)

    if request.method == "POST":
        print("posted")
        for answer in models.StudentAnswer.objects.filter(student=request.user, quiz=quiz):
            answer.delete()
        try:
            for question in questions:
                print(question.question_number)
                answer_text = request.POST.get(f"q{question.question_number}")
                answer = models.Answer.objects.get(answer_text=answer_text, question=question)
                new_student_answer = models.StudentAnswer.objects.create(
                    student=request.user,
                    question=question,
                    quiz=quiz,
                    chosen_answer=answer
                )
                new_student_answer.save()
                if answer.is_correct:
                    print("yes")
                else:
                    print("no")
            student_answers = models.StudentAnswer.objects.filter(student=request.user, quiz=quiz)
            total_marks = student_answers.filter(chosen_answer__is_correct=True).count()
            print(total_marks)
            saved_student_marks = models.StudentQuizMark.objects.get(quiz=quiz, user=request.user)
            saved_student_marks.final_score = total_marks
            saved_student_marks.date_completed = datetime.datetime.now()
            saved_student_marks.save()
            messages.success(request, "Answers submitted Successfully")
            return redirect('quiz_summary', community_name=community_name, quiz_title=quiz.title)
        except models.Answer.DoesNotExist:
            messages.warning(request, "Answer all questions")
    if models.StudentQuizMark.objects.filter(quiz=quiz, user=request.user, attempted=True).exists():
        messages.info(request, "Quiz Attempted Already")
        print("hey")
        return redirect('quiz_summary', community_name=community_name, quiz_title=quiz.title)
    new_student_quiz_mark = models.StudentQuizMark.objects.create(
        user=request.user,
        attempted=True,
        final_score=None,
        date_completed=datetime.datetime.now(),
        quiz=quiz,
        total_score_for_quiz=models.Question.objects.filter(quiz_it_belongs_to=quiz).count()
    )
    new_student_quiz_mark.save()
    context = {
        'questions': questions,
        'name': quiz.title,
        'community_name': community_name,
        'answers': answers,
        'modules': modules,
    }
    return render(request, "layouts/quiz/quiz_details.html", context=context)


def add_quiz(request, community_name):
    community = models.Community.objects.get(name=community_name)
    modules = models.Module.objects.filter(community_it_belongs_to=community)
    form = forms.AddQuizForm()
    if request.method == "POST":
        form = forms.AddQuizForm(request.POST)
        if form.is_valid():
            quiz_number = form.cleaned_data["quiz_number"]
            title = form.cleaned_data["quiz_title"]
            description = form.cleaned_data["quiz_description"]

            new_quiz = models.Quiz.objects.create(
                quiz_number=quiz_number,
                title=title,
                description=description,
                community_it_belongs_to=community,
            )
            new_quiz.save()
            messages.success(request, "Quiz Added")
            return redirect('add_quiz', community_name=community_name)
    context = {
        'community_name': community_name,
        'name': community_name,
        'form': form,
        'modules': modules
    }
    return render(request, "layouts/quiz/add_quiz.html", context=context)


def edit_quiz(request, community_name, pk):
    community = models.Community.objects.get(name=community_name)
    quiz = models.Quiz.objects.get(id=pk, community_it_belongs_to=community)
    modules = models.Module.objects.filter(community_it_belongs_to=community)
    form = forms.AddQuizForm(
        initial={
            'quiz_title': quiz.title,
            'quiz_number': quiz.quiz_number,
            'quiz_description': quiz.description
        }
    )
    if request.method == "POST":
        form = forms.AddQuizForm(request.POST)
        if form.is_valid():
            quiz_number = form.cleaned_data["quiz_number"]
            title = form.cleaned_data["quiz_title"]
            description = form.cleaned_data["quiz_description"]

            quiz.quiz_number = quiz_number
            quiz.title = title
            quiz.description = description
            quiz.save()
            messages.success(request, "Quiz Details Edited")
            return redirect('manage_quiz', community_name=community_name)
    context = {
        'community_name': community_name,
        'name': community_name,
        'form': form,
        'modules': modules
    }
    return render(request, "layouts/quiz/add_quiz.html", context=context)


def change_quiz_stat(request, community_name, pk):
    community = models.Community.objects.get(name=community_name)
    quiz = models.Quiz.objects.get(id=pk, community_it_belongs_to=community)
    quiz.status = "Dead" if quiz.status == "Active" else "Active"
    quiz.save()
    print(quiz.status)
    messages.success(request, "Quiz status Changed")
    return redirect('manage_quiz', community_name=community_name)


def quiz_manager(request, community_name):
    community = models.Community.objects.get(name=community_name)
    quizzes = models.Quiz.objects.filter(community_it_belongs_to=community).order_by('date_posted').reverse()
    modules = models.Module.objects.filter(community_it_belongs_to=community)
    context = {
        'community_name': community_name,
        'name': community_name,
        'quizzes': quizzes,
        'modules': modules
    }
    return render(request, "layouts/quiz/manage_quiz.html", context=context)


def student_quiz_scores(request, community_name, pk):
    community = models.Community.objects.get(name=community_name)
    quiz = models.Quiz.objects.get(id=pk)
    students_quiz_mark = models.StudentQuizMark.objects.filter(quiz=quiz, quiz__community_it_belongs_to=community)
    modules = models.Module.objects.filter(community_it_belongs_to=community)
    context = {
        'student_marks': students_quiz_mark,
        'community_name': community_name,
        'name': community_name,
        'quiz_title': quiz.title,
        'modules': modules
    }
    return render(request, "layouts/quiz/quiz_scores.html", context=context)


def add_question(request, community_name, quiz_id):
    community = models.Community.objects.get(name=community_name)
    quiz = models.Quiz.objects.get(id=quiz_id)
    modules = models.Module.objects.filter(community_it_belongs_to=community)

    question_form = forms.AddQuestionForm()
    answer_form = forms.AnswerFormSet()

    if request.method == 'POST':
        print(request.POST)
        question_form = forms.AddQuestionForm(request.POST)
        answer_form = forms.AnswerFormSet(request.POST)

        if question_form.is_valid() and answer_form.is_valid():
            print(answer_form.cleaned_data)
            question_text = question_form.cleaned_data["question_text"]
            question_number = question_form.cleaned_data["question_number"]

            new_question = models.Question.objects.create(
                quiz_it_belongs_to=quiz,
                question_number=question_number,
                question_text=question_text
            )
            new_question.save()

            # Save each answer with its relationship to the question
            for form in answer_form:
                question = models.Question.objects.get(question_text=question_text)
                answer_text = form.cleaned_data["answer_text"]
                is_correct = form.cleaned_data["is_correct"]
                print(is_correct)
                new_answer = models.Answer.objects.create(
                    answer_text=answer_text,
                    is_correct=is_correct,
                    question=question
                )
                new_answer.save()
            messages.success(request, "Question saved")
            return redirect('add_question', community_name=community.name, quiz_id=quiz.id)
        else:
            print(answer_form.errors)
    context = {
        'name': community_name,
        'community_name': community_name,
        'question_form': question_form,
        'answer_form_set': answer_form,
        'quiz_title': quiz.title,
        'modules': modules,
        'action': 'adding'
    }

    return render(request, "layouts/quiz/add_questions.html", context=context)


def quiz_score_page(request, community_name, quiz_title):
    community = models.Community.objects.get(name=community_name)
    student = models.CustomUser.objects.get(id=request.user.id)
    quiz = models.Quiz.objects.get(title=quiz_title)
    student_quiz_mark = models.StudentQuizMark.objects.get(quiz=quiz, user=student, attempted=True)
    modules = models.Module.objects.filter(community_it_belongs_to=community)
    context = {
        'quiz_mark': student_quiz_mark,
        'quiz': quiz,
        'name': community.name,
        'community_name': community.name,
        'modules': modules
    }
    return render(request, "layouts/quiz/after_quiz_page.html", context=context)


def edit_quiz_question(request, community_name, quiz_title, question_id):
    # Get community, quiz, and question instances
    community = models.Community.objects.get(name=community_name)
    quiz = models.Quiz.objects.get(title=quiz_title)
    question = models.Question.objects.get(id=question_id)
    modules = models.Module.objects.filter(community_it_belongs_to=community)

    # Get initial data for question form and answer formset
    initial_question_data = {
        'question_text': question.question_text,
        'question_number': question.question_number
    }
    initial_answers = models.Answer.objects.filter(question=question)

    # Initialize question form and answer formset with initial data
    question_form = forms.AddQuestionForm(initial=initial_question_data)
    AnswerFormSet = modelformset_factory(models.Answer, fields=('answer_text', 'is_correct'), extra=0)
    formset = AnswerFormSet(queryset=initial_answers)

    if request.method == "POST":
        question_form = forms.AddQuestionForm(request.POST)
        formset = AnswerFormSet(request.POST, queryset=initial_answers)

        if question_form.is_valid():
            question_text = question_form.cleaned_data["question_text"]
            question_number = question_form.cleaned_data["question_number"]

            question.question_number = question_number
            question.question_text = question_text
            question.save()

        print(formset)
        for form in formset:
            print(form)
        if formset.is_valid():
            formset.save()
            messages.success(request, "Question and Answers Edited Successfully")
            return redirect('quiz_questions', community_name=community_name, quiz_title=quiz.title)
        else:
            print("Formset not valid")
            print(formset.errors)

    # Apply formset field classes
    for form in formset:
        form.fields['answer_text'].widget.attrs['class'] = 'form-control'
        form.fields['is_correct'].widget.attrs['class'] = 'form-check-input correct_ans'
        form.fields['is_correct'].widget.attrs['name'] = 'correct_ans'

    # Prepare context data
    modules = models.Module.objects.filter(community_it_belongs_to=community)
    context = {
        'community_name': community_name,
        'question_form': question_form,
        'answer_form_set': formset,
        'quiz_title': quiz.title,
        'modules': modules,
        'name': community_name
    }
    return render(request, "layouts/quiz/add_questions.html", context=context)


def display_quiz_question(request, community_name, quiz_title):
    community = models.Community.objects.get(name=community_name)
    quiz = models.Quiz.objects.get(title=quiz_title)
    modules = models.Module.objects.filter(community_it_belongs_to=community)
    questions = models.Question.objects.filter(quiz_it_belongs_to=quiz)
    answers = models.Answer.objects.filter(question__in=questions)

    context = {
        'quiz': quiz,
        'modules': modules,
        'questions': questions,
        'community_name': community_name,
        'name': community_name,
        'answers': answers
    }

    return render(request, "layouts/quiz/quiz_questions.html", context=context)


