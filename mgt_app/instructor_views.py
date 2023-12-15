import datetime

import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from mgt_app import models, forms


def assign_instructor(request):
    if request.user.role != "Admin":
        messages.error(request, "Denied")
        return redirect('home')
    if request.method == "POST":
        form = forms.AssignInstructorForm(request.POST)
        if form.is_valid():
            instructor = form.cleaned_data["instructor"]
            co_instructor = form.cleaned_data["co_instructor"]
            community = form.cleaned_data["community"]

            print(instructor)
            print(type(instructor))

            m_instructor = models.CustomUser.objects.get(id=instructor.id)
            m_co_instructor = models.CustomUser.objects.get(id=co_instructor.id)
            m_community = models.Community.objects.get(name=community)

            m_instructor.role = "Instructor"
            m_co_instructor.role = "Co-Instructor"

            m_instructor.save()
            m_co_instructor.save()

            m_community.instructor = instructor
            m_community.co_instructor = co_instructor

            m_community.save()
            messages.success(request, "Instructors Assigned Successfully")
            return redirect('assign_instructor')
    form = forms.AssignInstructorForm()
    context = {
        'form': form,
        'community_name': 'Programming Community'
    }
    return render(request, "layouts/instructors/assign.html", context=context)



def instructors_list(request):
    if request.user.role != "Admin":
        messages.error(request, "Denied")
        return redirect('home')
    instructors = models.CustomUser.objects.filter(role__in=['Instructor', 'Co-Instructor'])
    communities = models.Community.objects.all()
    context = {
        'instructors': instructors,
        'communities': communities
    }
    return render(request, "layouts/instructors/list.html", context=context)


