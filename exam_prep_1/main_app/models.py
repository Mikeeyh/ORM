from django.db import models

from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from main_app.managers import DirectorManager
from main_app.mixins import LastUpdatedMixin, IsAwardedMixin

"""WITHOUT MIXINS"""


# class BasePerson(models.Model):
#     class Meta:
#         abstract = True
#
#     full_name = models.CharField(
#         max_length=120,
#         validators=[
#             MinLengthValidator(2),
#         ]
#     )
#
#     birth_date = models.DateField(
#         default='1900-01-01'
#     )
#
#     nationality = models.CharField(
#         max_length=50,
#         default='Unknown'
#     )
#
#     def __str__(self):
#         return self.full_name
#
#
# class Director(BasePerson):
#     years_of_experience = models.SmallIntegerField(
#         validators=[
#             MinValueValidator(0)
#         ],
#         default=0
#     )
#
#
# class Actor(BasePerson):
#     is_awarded = models.BooleanField(
#         default=False
#     )
#
#     last_updated = models.DateTimeField(
#         auto_now=True
#     )
#
#
# class Movie(models.Model):
#     class GenreChoices(models.TextChoices):
#         ACTION = 'Action', 'Action'
#         COMEDY = 'Comedy', 'Comedy'
#         DRAMA = 'Drama', 'Drama'
#         OTHER = 'Other', 'Other'
#
#     title = models.CharField(
#         max_length=150,
#         validators=[
#             MinLengthValidator(5)
#         ]
#     )
#
#     release_date = models.DateField()
#
#     storyline = models.TextField(
#         blank=True,
#         null=True
#     )
#
#     genre = models.CharField(
#         max_length=6,
#         choices=GenreChoices.choices,
#         default='Other'
#     )
#
#     rating = models.DecimalField(
#         max_digits=3,
#         decimal_places=1,
#         validators=[
#             MinValueValidator(0.0),
#             MaxValueValidator(10.0)
#         ],
#         default=0.0
#     )
#
#     is_classic = models.BooleanField(
#         default=False
#     )
#
#     is_awarded = models.BooleanField(
#         default=False
#     )
#
#     last_updated = models.DateTimeField(
#         auto_now=True
#     )
#
#     director = models.ForeignKey(
#         Director,
#         on_delete=models.CASCADE,
#         related_name='director_movies'
#     )
#
#     starring_actor = models.ForeignKey(
#         Actor,
#         on_delete=models.SET_NULL,
#         related_name='starring_movies',
#         null=True,
#         blank=True
#     )
#
#     actors = models.ManyToManyField(
#         Actor,
#         related_name='actor_movies'
#     )
#
#     def __str__(self):
#         return self.title

"""WITH MIXINS"""


class BasePerson(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2)])
    birth_date = models.DateField(default='1900-01-01')
    nationality = models.CharField(
        max_length=50,
        default='Unknown')

    def __str__(self):
        return self.full_name

    class Meta:
        abstract = True


class Director(BasePerson):
    years_of_experience = models.SmallIntegerField(
        default=0,
        validators=[MinValueValidator(0)])

    objects = DirectorManager()


class Actor(LastUpdatedMixin, IsAwardedMixin, BasePerson):
    pass


class Movie(LastUpdatedMixin, IsAwardedMixin):
    GENRE_CHOICES = [
        ('Action', 'Action'),
        ('Comedy', 'Comedy'),
        ('Drama', 'Drama'),
        ('Other', 'Other'),
    ]

    title = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(5)])

    release_date = models.DateField()

    storyline = models.TextField(null=True, blank=True)

    genre = models.CharField(
        max_length=6,
        choices=GENRE_CHOICES,
        default='Other')

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        default=0.0)

    is_classic = models.BooleanField(default=False)

    director = models.ForeignKey(Director,
                                 on_delete=models.CASCADE,
                                 related_name='director_movies')
    starring_actor = models.ForeignKey(Actor,
                                       on_delete=models.SET_NULL,
                                       related_name='starring_movies',
                                       null=True, blank=True)
    actors = models.ManyToManyField(Actor,
                                    related_name='actor_movies')

    def __str__(self):
        return self.title
