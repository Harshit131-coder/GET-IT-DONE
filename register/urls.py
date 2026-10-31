from django.urls import path
from . import views

urlpatterns = [
    path("reg",views.register, name="reg"),
    path("login",views.login, name="login"),
    path("logout",views.logout, name="logout"),
    path("profile",views.profile, name="profile"),
    path("update_profile",views.update_profile, name='update_profile'),
    path("staffreg",views.staffreg, name='staffreg'),
   
]