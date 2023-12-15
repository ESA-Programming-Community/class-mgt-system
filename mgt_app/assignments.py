import datetime

import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from mgt_app import models, forms


def add_assignment(request, community_name):
    community = models.Community.objects.get(name=community_name)
    user = models.CustomUser.objects.get(id=request.user.id)
    assignment_count = models.Assignment.objects.filter(community_it_belongs_to=community).count()
    form = forms.AddAssignmentForm(community=community, initial={
        'assignment_number': assignment_count + 1
    })

    if request.method == "POST":
        form = forms.AddAssignmentForm(data=request.POST, community=community)
        if form.is_valid():
            title = form.cleaned_data["title"]
            instruction = form.cleaned_data["instruction"]
            reference = form.cleaned_data["module_referenced"]
            deadline = form.cleaned_data["deadline"]

            print(title)
            print(instruction)
            print(reference)
            print(deadline)

            new_assignment = models.Assignment.objects.create(
                user_posted=request.user,
                community_it_belongs_to=community,
                assignment_title=title,
                assignment_instruction=instruction,
                module_it_belongs_to=reference,
                deadline=deadline
            )
            new_assignment.save()
            messages.success(request, "Assignment Added")
            return redirect('add_assignment', community_name=community_name)
        else:
            print("not valid")
    context = {
        'form': form,
        'name': community_name,
        'community_name':community_name,
        'action': 'adding'
    }

    return render(request, "layouts/assignments/add_assignment.html", context=context)


def manage_assignments(request, community_name):
    community = models.Community.objects.get(name=community_name)
    user = models.CustomUser.objects.get(id=request.user.id)
    assignments = models.Assignment.objects.filter(community_it_belongs_to=community)

    context = {
        'name': community_name,
        'community_name': community_name,
        'assignments': assignments
    }

    return render(request, "layouts/assignments/manage_assignments.html", context=context)




