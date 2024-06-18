import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from mgt_app import models


@login_required(login_url='login')
# Create your views here.
def home(request):
    user = models.CustomUser.objects.get(id=request.user.id)
    if user.approved:
        communities = models.Community.objects.all()
        context = {
            'comms': communities
        }
        return render(request, "layouts/community_overview.html", context=context)
    else:
        messages.success(request, 'You are not approved to access this page')
        return redirect("home")


@login_required(login_url='login')
def join_community(request, community_name):
    user = models.CustomUser.objects.get(id=request.user.id)
    print(community_name)
    community = models.Community.objects.get(name=community_name)
    print(community.name)
    print(community.description)
    print(community.co_instructor)
    if user in community.members.all():
        print("already in community")
        return redirect('dashboard', community_name=community_name)
    community.members.add(user)
    new_requirement = models.RequirementFulfillment.objects.create(
        student=user,
        community=community,
        fulfilled=False,
    )
    new_requirement.save()
    messages.success(request, f"You have joined the {community.name}")
    return redirect("dashboard", community_name=community_name)


@login_required(login_url='login')
def dashboard(request, community_name):
    community = models.Community.objects.get(name=community_name)
    print(community.co_instructor)
    community_members = community.members.all()
    modules = models.Module.objects.filter(community_it_belongs_to=community)
    requirement_fulfilled = models.RequirementFulfillment.objects.filter(community=community, student=request.user).first().fulfilled
    context = {
        'name': community.name,
        'instructor': f"{community.instructor.first_name} {community.instructor.last_name}",
        'co_instructor': f"{community.co_instructor.first_name} {community.co_instructor.last_name}",
        'description': community.description,
        'link': community.group_link,
        'members': community_members,
        'modules': modules,
        'community_name': community_name,
        'requirements': community.requirements if community.requirements else None,
        'requirement_fulfilled': requirement_fulfilled
    }
    return render(request, "layouts/index.html", context=context)


@login_required(login_url='login')
def module_details(request, community_name, module_name):
    community = models.Community.objects.get(name=community_name)
    module = models.Module.objects.get(name=module_name)
    lessons = models.Lesson.objects.filter(module_it_belongs_to=module).order_by('lesson_number')
    lesson_count = lessons.count()
    modules = models.Module.objects.filter(community_it_belongs_to=community)
    user = models.CustomUser.objects.get(id=request.user.id)
    print(user)
    print(community.instructor)

    if request.method == "POST":
        if community.instructor == user:
            print(user)
            print(community.instructor)
            lesson_number = request.POST.get("lesson-number")
            title = request.POST.get("title")
            description = request.POST.get("desc")

            if not models.Lesson.objects.filter(lesson_number=lesson_number).exists():
                new_lesson = models.Lesson.objects.create(
                    module_it_belongs_to=module,
                    lesson_number=lesson_number,
                    title=title,
                    description=description
                )
                new_lesson.save()
                messages.success(request, "Lesson Added Successfully")
                return redirect('module_details', community_name=community_name, module_name=module.name)
        else:
            messages.warning(request, "Access Denied")
            return redirect('module_details', community_name=community_name, module_name=module.name)

    context = {
        'name': f"Module {module.module_number} - {module.name}",
        'community_name': community.name,
        'community': community,
        'module_name': module.name,
        'lessons': lessons,
        'modules': modules,
        'lesson_count': lesson_count + 1
    }
    return render(request, "layouts/module_lessons.html", context=context)


@login_required(login_url='login')
def lesson_resources(request, community_name, module_name, lesson_title):
    community = models.Community.objects.get(name=community_name)
    module = models.Module.objects.get(name=module_name)
    modules = models.Module.objects.filter(community_it_belongs_to=community)
    lesson = models.Lesson.objects.get(title=lesson_title)
    resources = models.Resource.objects.filter(lesson_it_belongs_to=lesson)
    user = models.CustomUser.objects.get(id=request.user.id)

    if request.method == "POST":
        if community.instructor == user:
            title = request.POST.get("title")
            link = request.POST.get("link")
            description = request.POST.get("desc")

            new_resource = models.Resource.objects.create(
                title=title,
                link=link,
                description=description,
                lesson_it_belongs_to=lesson
            )
            new_resource.save()
            messages.success(request, "Resource Added")
            return redirect('lesson_resources', community_name=community_name, module_name=module_name, lesson_title=lesson.title)
        else:
            messages.error(request, "Access Denied")
            return redirect('lesson_resources', community_name=community_name, module_name=module_name, lesson_title=lesson.title)

    context = {
        'name': f"Module {module.module_number} - {module.name}",
        'community_name': community.name,
        'community': community,
        'module_name': module.name,
        'lesson_name': lesson.title,
        'resources': resources,
        'modules': modules,
    }

    return render(request, "layouts/lesson_resources.html", context=context)

@login_required(login_url='login')
def lesson_resource_player(request, community_name, pk):
    community = models.Community.objects.get(name=community_name)
    resource = models.Resource.objects.get(id=pk, lesson_it_belongs_to__module_it_belongs_to__community_it_belongs_to=community)
    modules = models.Module.objects.filter(community_it_belongs_to=community)
    context = {
        'resource': resource,
        'community_name': community_name,
        'name': f"{resource.title} Video",
        'modules': modules
    }
    return render(request, "layouts/resource_link_player.html", context=context)


@login_required(login_url='login')
def delete_lesson(request, community_name, lesson_name):
    community = models.Community.objects.get(name=community_name)
    lesson = models.Lesson.objects.get(title=lesson_name)
    module_name = lesson.module_it_belongs_to
    user = models.CustomUser.objects.get(id=request.user.id)
    instructor = community.instructor

    if user == instructor:
        lesson.delete()
        messages.success(request, "Lesson Deleted")
        return redirect('module_details', community_name=community_name, module_name=module_name.name)
    else:
        messages.warning(request, "Access Denied")
        return redirect(home)

@login_required(login_url='login')
def unapproved_students(request):
    if request.user.is_superuser:
        user = models.CustomUser.objects.get(id=request.user.id)
        unapproved_students_list = models.CustomUser.objects.filter(approved=False, student_class=user.student_class)
        context = {'students': unapproved_students_list}
        return render(request, "layouts/pending_approvals.html", context=context)
    else:
        messages.success(request, "Access Denied..")
        return redirect("home")

@login_required(login_url='login')
def approve_student(request, pk):
    if request.user.is_superuser:
        user = models.CustomUser.objects.get(id=request.user.id)
        student_class = user.student_class
        student_to_be_approved = models.CustomUser.objects.get(id=pk, student_class=student_class)
        name = student_to_be_approved.first_name + " " + student_to_be_approved.last_name
        phone = student_to_be_approved.phone_number
        print(phone)
        student_to_be_approved.approved = True
        student_to_be_approved.save()
        messages.success(request, f"{name} has been approved.")
        message = f"Hello {name}, Your account for the Classroom has been approved. You can log in now to join your classroom."
        url = f"https://sms.arkesel.com/sms/api?action=send-sms&api_key=cWhNWkhHcEV0SEZNTFpvT3B0V2o&to=233{phone}&from=Classroom&sms={message}"
        response = requests.get(url=url)
        print(response.json())
        return redirect('pending_approvals')
    else:
        messages.warning(request, "Access Denied..")
        return redirect("home")

@login_required(login_url='login')
def admin_page_duties(request):
    return render(request, "admin_page.html")

