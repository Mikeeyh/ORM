from django.core.validators import MinLengthValidator, RegexValidator, MinValueValidator
from django.db import models

from main_app.managers import CustomAstronautManager


class Astronaut(models.Model):
    name = models.CharField(
        max_length=120,
        validators=[
            MinLengthValidator(2)
        ],
    )

    phone_number = models.CharField(
        max_length=15,
        unique=True,
        validators=[
            RegexValidator(regex=r'^\d+$')
        ],
    )

    is_active = models.BooleanField(
        default=True,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    spacewalks = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0)
        ],
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    objects = CustomAstronautManager()

    def __str__(self):
        return self.name


class Spacecraft(models.Model):
    name = models.CharField(
        max_length=120,
        validators=[
            MinLengthValidator(2)
        ],
    )

    manufacturer = models.CharField(
        max_length=100,
    )

    capacity = models.SmallIntegerField(
        validators=[
            MinValueValidator(1)
        ],
    )

    weight = models.FloatField(
        validators=[
            MinValueValidator(0.0)
        ]
    )

    launch_date = models.DateField(

    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )


class Mission(models.Model):

    class Statuses(models.TextChoices):
        PLANNED = 'Planned', 'Planned'
        ONGOING = 'Ongoing', 'Ongoing'
        COMPLETED = 'Completed', 'Completed'

    name = models.CharField(
        max_length=120,
        validators=[
            MinLengthValidator(2)
        ],
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=9,
        choices=Statuses.choices,
        default=Statuses.PLANNED,
    )

    launch_date = models.DateField(

    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    spacecraft = models.ForeignKey(
        to=Spacecraft,
        on_delete=models.CASCADE,
    )

    astronauts = models.ManyToManyField(
        to=Astronaut,
        related_name='missions',
    )

    commander = models.ForeignKey(
        to=Astronaut,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='commander_missions',
    )
