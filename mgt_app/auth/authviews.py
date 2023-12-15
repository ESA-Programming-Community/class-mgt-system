from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from mgt_app import forms, models


def sign_up(request):
    if request.user.is_authenticated:
        messages.warning(request, "Log out to sign up for a different account.")
        return redirect('home')
    form = forms.CustomUserForm()
    if request.method == "POST":
        form = forms.CustomUserForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, f"Sign Up Successful. Log in to continue.")
            return redirect('login')
        else:
            print("nope")
    context = {'form': form}
    return render(request, "auth/register.html", context=context)


# def instructor_sign_up(request):
#     if request.user.is_authenticated:
#         messages.warning(request, "Log out to sign up for a different account.")
#         return redirect('home')
#     form = forms.CustomUserForm()
#     if request.method == "POST":
#         form = forms.CustomUserForm(data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data["username"]
#             community = request.POST.get("community")
#             form.save()
#             comm
#
#
#         else:
#             print("nope")
#     context = {'form': form}
#     return render(request, "auth/class_rep_signup.html", context=context)


def login_page(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('home')
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            password = request.POST.get('pass')

            print(name)
            print(password)

            user = authenticate(request, username=name, password=password)
            print(user)
            if user:
                login(request, user)
                messages.success(request, 'Log in Successful')
                if request.user.role == "Admin":
                    return redirect('admin_page')
                elif request.user.role == "Instructor" or request.user.role == "Co-Instructor":
                    try:
                        community = models.Community.objects.get(instructor=request.user)
                    except models.Community.DoesNotExist:
                        community = models.Community.objects.get(co_instructor=request.user)
                    return redirect('dashboard', community_name=community.name)
                else:
                    return redirect('home')
            else:
                print("here")
                messages.info(request, 'Invalid username or password')
                return redirect('login')
    return render(request, "auth/login.html")


@login_required(login_url='login')
def logout_page(request):
    logout(request)
    messages.success(request, "Log out successful")
    return redirect('home')


