from django.urls import path
from . import views
urlpatterns = [
    path('logout/',views.logoutUser,name="logout"),
    path('login/',views.loginUser,name = "login"),
    path('signup/',views.signUp,name = "signup"),
    path('dashboard/',views.dashboard,name="dashboard")
]