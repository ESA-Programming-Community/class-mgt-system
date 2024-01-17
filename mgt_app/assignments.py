import datetime

import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils import timezone

from mgt_app import models, forms


def add_assignment(request, community_name):
    community = models.Community.objects.get(name=community_name)
    modules = models.Module.objects.filter(community_it_belongs_to=community)
    user = models.CustomUser.objects.get(id=request.user.id)
    assignment_count = models.Assignment.objects.filter(community_it_belongs_to=community).count()
    form = forms.AddAssignmentForm(community=community, initial={
        'assignment_number': assignment_count + 1
    })

    if request.method == "POST":
        form = forms.AddAssignmentForm(data=request.POST, community=community)
        if form.is_valid():
            number = form.cleaned_data["assignment_number"]
            title = form.cleaned_data["title"]
            instruction = form.cleaned_data["instruction"]
            reference = form.cleaned_data["module_referenced"]
            deadline = form.cleaned_data["deadline"]
            mode = form.cleaned_data["mode_of_submission"]
            sub_format = form.cleaned_data["preferred_submission_format"]

            print(title)
            print(instruction)
            print(reference)
            print(deadline)

            new_assignment = models.Assignment.objects.create(
                assignment_number=number,
                user_posted=request.user,
                community_it_belongs_to=community,
                assignment_title=title,
                assignment_instruction=instruction,
                module_it_belongs_to=reference,
                deadline=deadline,
                mode_of_submission=mode,
                preferred_submission_format=sub_format
            )
            new_assignment.save()
            messages.success(request, "Assignment Added")
            return redirect('add_assignment', community_name=community_name)
        else:
            print("not valid")
    context = {
        'form': form,
        'name': community_name,
        'community_name': community_name,
        'action': 'adding',
        'modules': modules,
    }

    return render(request, "layouts/assignments/add_assignment.html", context=context)


def edit_assignment(request, community_name, assignment_title):
    community = models.Community.objects.get(name=community_name)
    user = models.CustomUser.objects.get(id=request.user.id)
    assignment_to_be_edited = models.Assignment.objects.get(assignment_title=assignment_title)
    modules = models.Module.objects.filter(community_it_belongs_to=community)
    form = forms.AddAssignmentForm(community=community, initial={
        'assignment_number': assignment_to_be_edited.assignment_number,
        'title': assignment_to_be_edited.assignment_title,
        'instruction': assignment_to_be_edited.assignment_instruction,
        'deadline': assignment_to_be_edited.deadline,
        'module_referenced': assignment_to_be_edited.module_it_belongs_to,
        'preferred_submission_format': assignment_to_be_edited.preferred_submission_format,
        'mode_of_submission': assignment_to_be_edited.mode_of_submission
    })

    if request.method == "POST":
        form = forms.AddAssignmentForm(data=request.POST, community=community)
        if form.is_valid():
            number = form.cleaned_data["assignment_number"]
            title = form.cleaned_data["title"]
            instruction = form.cleaned_data["instruction"]
            deadline = form.cleaned_data["deadline"]
            reference = form.cleaned_data['module_referenced']
            mode = form.cleaned_data["mode_of_submission"]
            sub_format = form.cleaned_data["preferred_submission_format"]

            assignment_to_be_edited.assignment_number = number
            assignment_to_be_edited.assignment_title = title
            assignment_to_be_edited.assignment_instruction = instruction
            assignment_to_be_edited.deadline = deadline
            assignment_to_be_edited.module_it_belongs_to = reference
            assignment_to_be_edited.mode_of_submission = mode
            assignment_to_be_edited.preferred_submission_format = sub_format
            assignment_to_be_edited.save()
            messages.success(request, "Assignment Edited")
            return redirect('manage_assignment', community_name=community_name)

    context = {
        'name': community_name,
        'community_name': community_name,
        'form': form,
        'action': 'editing',
        'title': assignment_to_be_edited.assignment_title,
        'modules': modules,
    }

    return render(request, "layouts/assignments/add_assignment.html", context=context)


def change_stat(request, community_name, assignment_title):
    assignment = models.Assignment.objects.get(assignment_title=assignment_title)
    assignment.status = False if assignment.status else True
    assignment.save()
    messages.success(request, "Assignment Status Changed")
    return redirect('manage_assignment', community_name=community_name)


def delete_assignment(request, community_name, assignment_title):
    assignment = models.Assignment.objects.get(assignment_title=assignment_title)
    assignment.delete()
    messages.success(request, "Assignment Deleted")
    return redirect('manage_assignment', community_name=community_name)


def manage_assignments(request, community_name):
    community = models.Community.objects.get(name=community_name)
    user = models.CustomUser.objects.get(id=request.user.id)
    assignments = models.Assignment.objects.filter(community_it_belongs_to=community)
    modules = models.Module.objects.filter(community_it_belongs_to=community)

    context = {
        'name': community_name,
        'community_name': community_name,
        'assignments': assignments,
        'modules': modules,
    }

    return render(request, "layouts/assignments/manage_assignments.html", context=context)


def student_page_assignments(request, community_name):
    community = models.Community.objects.get(name=community_name)
    user = models.CustomUser.objects.get(id=request.user.id)
    assignments = models.Assignment.objects.filter(community_it_belongs_to=community)
    modules = models.Module.objects.filter(community_it_belongs_to=community)

    context = {
        'name': community_name,
        'community_name': community_name,
        'assignments': assignments,
        'modules': modules,
    }

    return render(request, "layouts/assignments/assignments_page.html", context=context)


def assignment_detail(request, community_name, assignment_title):
    community = models.Community.objects.get(name=community_name)
    user = models.CustomUser.objects.get(id=request.user.id)
    assignment = models.Assignment.objects.get(community_it_belongs_to=community, assignment_title=assignment_title)
    modules = models.Module.objects.filter(community_it_belongs_to=community)
    try:
        submission = models.Submission.objects.get(assignment=assignment, user=user, assignment__community_it_belongs_to=community)
    except models.Submission.DoesNotExist:
        submission = None
    context = {
        'name': community_name,
        'community_name': community_name,
        'assignment': assignment,
        'modules': modules,
        'submission': submission
    }

    return render(request, "layouts/assignments/assignment_details.html", context=context)


def submission_page(request, community_name, assignment_title):
    community = models.Community.objects.get(name=community_name)
    user = models.CustomUser.objects.get(id=request.user.id)
    assignment = models.Assignment.objects.get(community_it_belongs_to=community, assignment_title=assignment_title)
    modules = models.Module.objects.filter(community_it_belongs_to=community)

    if models.Submission.objects.filter(user=user, assignment=assignment).exists():
        messages.success(request, "Your submission already exists")
        return redirect('assignments', community_name=community.name)
    if assignment.deadline and timezone.now() > assignment.deadline:
        # Deadline has passed
        messages.error(request, "Sorry, the deadline for this assignment has passed.")
        return redirect('assignment_detail', community_name=community_name, assignment_title=assignment.assignment_title)

    form = forms.SubmissionForm()

    if request.method == "POST":
        print(request.POST)
        print(request.FILES)
        form = forms.SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            file_data = form.cleaned_data.get('file_field')
            url_data = form.cleaned_data.get('url_field')
            text_data = form.cleaned_data.get('plain_text_field')
            student_note = form.cleaned_data.get('student_note')

            # Determine which field was submitted
            if file_data:
                submission_instance = models.Submission.objects.create(
                    assignment=assignment,
                    user=user,
                    submission_date=datetime.datetime.now(),
                    student_note=student_note,
                )
                submission_instance.save()
                submission_instance.save_uploaded_file(file_data)
                messages.success(request, "Your assignment has been submitted successfully")
                print("filesubmission")
                return redirect('assignments', community_name=community.name)
            elif url_data:
                submission_instance = models.Submission.objects.create(
                    assignment=assignment,
                    user=user,
                    submission_date=datetime.datetime.now(),
                    student_note=student_note,
                    url_submission=url_data
                )
                submission_instance.save()
                messages.success(request, "Your assignment has been submitted successfully")
                print("url data submitted")
                return redirect('assignments', community_name=community.name)
            elif text_data:
                submission_instance = models.Submission.objects.create(
                    assignment=assignment,
                    user=user,
                    submission_date=datetime.datetime.now(),
                    student_note=student_note,
                    text_submission=text_data
                )
                submission_instance.save()
                messages.success(request, "Your assignment has been submitted successfully")
                print("text data submitted")
                return redirect('assignments', community_name=community.name)
        else:
            print("not valid")
            print(form.errors)
    context = {
        'name': community_name,
        'community_name': community_name,
        'assignment': assignment,
        'form': form,
        'modules': modules,
    }

    return render(request, "layouts/assignments/submission_page.html", context=context)


def student_submissions(request, community_name):
    community = models.Community.objects.get(name=community_name)
    user = models.CustomUser.objects.get(id=request.user.id)
    # assignment = models.Assignment.objects.get(community_it_belongs_to=community)
    assignments = models.Assignment.objects.filter(submission__user=user)
    modules = models.Module.objects.filter(community_it_belongs_to=community)

    # Get all assignments
    assignments = models.Assignment.objects.filter(community_it_belongs_to=community)

    # Create a dictionary to store submissions grouped by assignment
    submissions_by_assignment = {}

    # Loop through each assignment to fetch related submissions
    for assignment in assignments:
        submissions = models.Submission.objects.filter(assignment=assignment, user=user)
        submissions_by_assignment[assignment] = submissions

    context = {
        'name': community_name,
        'community_name': community_name,
        'submissions_by_assignment': submissions_by_assignment,
        'modules': modules,
    }

    return render(request, "layouts/assignments/student_submissions.html", context=context)


def student_submission_detail(request, community_name, assignment_title, submission_id):
    community = models.Community.objects.get(name=community_name)
    user = models.CustomUser.objects.get(id=request.user.id)
    assignment = models.Assignment.objects.get(assignment_title=assignment_title, community_it_belongs_to=community)
    submission = models.Submission.objects.get(id=submission_id, user=request.user, assignment=assignment)
    modules = models.Module.objects.filter(community_it_belongs_to=community)

    context = {
        'name': community_name,
        'community_name': community_name,
        'submission': submission,
        'assignment': assignment,
        'modules': modules,
    }

    return render(request, "layouts/assignments/student_submission_details.html", context=context)


def submissions_for_instructor(request, community_name, assignment_title):
    community = models.Community.objects.get(name=community_name)
    user = models.CustomUser.objects.get(id=request.user.id)
    assignment = models.Assignment.objects.get(assignment_title=assignment_title, community_it_belongs_to=community)

    submissions = models.Submission.objects.filter(assignment=assignment)
    count = models.Submission.objects.filter(assignment=assignment).count()

    context = {
        'name': community.name,
        'community_name': community.name,
        'submissions': submissions,
        'assignment': assignment,
        'count': count
    }

    return render(request, "layouts/assignments/instructor_submissions.html", context=context)


def submission_detail_instructor(request, community_name, assignment_title, submission_id):
    community = models.Community.objects.get(name=community_name)
    user = models.CustomUser.objects.get(id=request.user.id)
    assignment = models.Assignment.objects.get(assignment_title=assignment_title, community_it_belongs_to=community)
    submission = models.Submission.objects.get(id=submission_id, assignment=assignment, assignment__community_it_belongs_to=community)

    if request.method == "POST":
        remarks = request.POST.get("remarks")
        submission.remarks = remarks
        print(remarks)
        submission.save()
        messages.success(request, "Remarks Updated")
        return redirect('sub_detail_instructor', community_name=community_name, assignment_title=assignment.assignment_title, submission_id=submission.id)


    context = {
        'name': community.name,
        'community_name': community.name,
        'submission': submission,
        'assignment': assignment
    }

    return render(request, "layouts/assignments/submission_detail_instructor.html", context=context)








