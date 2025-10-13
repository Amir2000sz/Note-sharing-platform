from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm,UserRegisterForm
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

