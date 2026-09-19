from django.contrib.auth.models import User
from django.db import models


class MuscleGroup(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    muscle_group = models.ForeignKey(
        MuscleGroup,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Workout(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.workout} - {self.exercise}'


class Set(models.Model):
    workout_exercise = models.ForeignKey(
        WorkoutExercise,
        on_delete=models.CASCADE
    )
    weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    repetitions = models.PositiveIntegerField(
        null=True,
        blank=True
    )
    distance = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True
    )

    def __str__(self):
        if self.weight:
            return f'{self.weight} кг × {self.repetitions}'
        elif self.distance:
            return f'{self.distance} км'