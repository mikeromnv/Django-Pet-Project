from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from workouts.forms import RegisterForm
from workouts.models import Workout, Exercise, WorkoutExercise


def home_view(request):
    if request.user.is_authenticated:
        return render(request, 'workouts/home.html')

    return redirect('login')

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )

            login(request, user)

            return redirect('home')
    else:
        form = RegisterForm()

    return render(
        request,
        'workouts/register.html',
        {'form': form}
    )

def login_view(request):
    error = None
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user=authenticate(
            request,
            username=username,
            password=password
        )
        if user is not None:
            login(request, user)
            return redirect('home')
        error = "Неверный логин или пароль"
    return render(
        request,
        'workouts/login.html',
        {'error': error}
    )

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def workout_list(request):
    workouts = Workout.objects.filter(
        user=request.user
    ).order_by('-id')

    return render(request, 'workouts/workout_list.html', {'workouts': workouts})

@login_required(login_url='login')
def workout_create(request):
    if request.method == "POST":
        name = request.POST['name']
        date = request.POST.get('date')

        if name=='':
            counts = len(Workout.objects.filter(user=request.user))
            name = f'Тренировка №{counts}'

        Workout.objects.create(
            name=name,
            date=date,
            user=request.user
        )

        return redirect('workout_list')

    return render(request, 'workouts/workout_create.html')

@login_required(login_url='login')
def workout_detail(request, workout_id):
    workout = get_object_or_404(
        Workout,
        id=workout_id,
        user=request.user
    )
    if request.method == "POST":
        exercise_id = request.POST['exercise']

        if exercise_id:
            exercise = get_object_or_404(
                Exercise,
                id=exercise_id,
            )

            WorkoutExercise.objects.create(
                workout=workout,
                exercise=exercise,
            )

        return redirect('workout_detail', workout_id=workout_id)

    exercises = Exercise.objects.all().order_by('name')

    workout_exercises = workout.workoutexercise_set.select_related('exercise')
    return render(
        request,
        'workouts/workout_detail.html',
        {'workout': workout, 'exercises': exercises, 'workout_exercises': workout_exercises}
    )

