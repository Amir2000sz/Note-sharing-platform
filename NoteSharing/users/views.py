from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm,UserRegisterForm,UserTagForm
from .models import UserTag
def logoutUser(request):
    logout(request)
    return redirect("Home")

def loginUser(request):
    error = ""
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect("Home")
        else:
            error = "Invalid user name or password"
    else:
        return render(request,"login.html",{"error":error})

def signUp(request):
    if request.user.is_authenticated:
        return redirect("Home")
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileForm(request.POST ,request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('login')
    else:
        user_form = UserRegisterForm()
        profile_form = ProfileForm()
    context = {"userForm":user_form,"profileForm":profile_form}
    return render(request,"signup.html",context=context)
@login_required
def dashboard(request):
    profile = request.user.profile
    if request.method == "POST":
        tag_form = UserTagForm(request.POST)
        if tag_form.is_valid():
            title = tag_form.cleaned_data["title"].strip()
            tag, _ = UserTag.objects.get_or_create(title=title)
            tag.profile.add(profile)
            return redirect("dashboard")
    
    context = {
        "user": request.user,
        "profile": profile,
        "tags": profile.usertag_set.all(),
        "tag_form": UserTagForm(),
    }
    return render(request,"dashboard.html",context=context)
# @login_required
# def AddUserTags(request):
#     profile = request.user.profile
#     if request.method == "POST":
#         tag_form = UserTagForm(request.POST)
#         if tag_form.is_valid():
#             title = tag_form.cleaned_data["title"].strip()
#             tag, _ = UserTag.objects.get_or_create(title=title)
#             tag.profile.add(profile)
#             return redirect("dashboard")
#     else:
#         tag_form = UserTagForm()
#     notes = getattr(profile, "note_set", []).all() if hasattr(profile, "note_set") else []
#     context = {
#         "user": request.user,
#         "profile": profile,
#         "notes": notes,
#         "tags": profile.usertag_set.all(),
#         "tag_form": tag_form,
#     }
#     return render(request,"dashboard.html",context=context)
