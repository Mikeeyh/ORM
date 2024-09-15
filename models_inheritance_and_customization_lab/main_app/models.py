from datetime import date

from django.core.exceptions import ValidationError
from django.db import models

# CUSTOM FILED:


class BooleanChoiceField(models.BooleanField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = ((True, 'Available'), (False, 'Not Available'))
        kwargs['default'] = True
        super().__init__(*args, **kwargs)


class Animal(models.Model):
    name = models.CharField(
        max_length=100,
    )

    species= models.CharField(
        max_length=100,
    )

    birth_date = models.DateField()

    sound = models.CharField(
        max_length=100,
    )

    @property
    def age(self):
        age = date.today() - self.birth_date
        return age.days // 365


class Mammal(Animal):
    fur_color = models.CharField(
        max_length=50,
    )


class Bird(Animal):
    wing_span = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )


class Reptile(Animal):
    scale_type = models.CharField(
        max_length=50,
    )


class Employee(models.Model):
    first_name = models.CharField(
        max_length=50,
    )

    last_name = models.CharField(
        max_length=50,
    )

    phone_number = models.CharField(
        max_length=10,
    )

    class Meta:  # For abstract class that does not have a table in DB
        abstract = True


class ZooKeeper(Employee):
    class Specialities(models.TextChoices):
        MAMMALS = "Mammals", "Mammals"
        BIRDS = "Birds", "Birds"
        REPTILES = "Reptiles", "Reptiles"
        OTHERS = "Others", "Others"

    specialty = models.CharField(
        max_length=10,
        choices=Specialities.choices,
    )

    managed_animals = models.ManyToManyField(
        to=Animal,
    )

    def clean(self):  # 'clean' is used for validation before saving to DB
        if self.specialty not in ZooKeeper.Specialities:  # We check if the choice is valid
            raise ValidationError("Specialty must be a valid choice.")


class Veterinarian(Employee):
    license_number = models.CharField(
        max_length=10,
    )

    availability = BooleanChoiceField()


class ZooDisplayAnimal(Animal):
    class Meta:
        proxy = True  # this method would have the same thing as Animal. Then we can add custom methods in it.

    def display_info(self):
        return (f"Meet {self.name}! Species: {self.species}, born {self.birth_date}. "
                f"It makes a noise like '{self.sound}'.")

    def is_endangered(self):
        endangered_species = ["Cross River Gorilla", "Orangutan", "Green Turtle"]
        if self.species in endangered_species:
            result = f"{self.species} is at risk!"
        else:
            result = f"{self.species} is not at risk."
        return result
