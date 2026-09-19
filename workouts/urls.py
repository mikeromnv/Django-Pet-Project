from django.urls import path

from workouts.views import *

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path('', home_view, name='home'),
    path('logout/', logout_view, name='logout'),
    path('workout/', workout_list, name='workout_list'),
    path('workouts/create/', workout_create, name='workout_create'),
]