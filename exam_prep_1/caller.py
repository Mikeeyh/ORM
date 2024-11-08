import os
import django
from django.db.models.functions import Coalesce

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Director, Actor, Movie
from django.db.models import Q, Count, Avg, F


def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None:
        return ''

    query_name = Q(full_name__icontains=search_name)
    query_nationality = Q(nationality__icontains=search_nationality)

    if search_name is not None and search_nationality is not None:
        query = Q(query_name & query_nationality)
    elif search_name is not None:
        query = query_name
    else:
        query = query_nationality

    directors = Director.objects.filter(query).order_by('full_name')

    if not directors:
        return ''

    result = []
    for director in directors:
        result.append(f"Director: {director.full_name}, "
                      f"nationality: {director.nationality}, "
                      f"experience: {director.years_of_experience}")

    return '\n'.join(result)


def get_top_director():  # using the custom manager
    director = Director.objects.get_directors_by_movies_count().first()
    if not director:
        return ''
    return f"Top Director: {director.full_name}, movies: {director.movies_count}."  # taking 'movies_count' from the manager


def get_top_actor():
    actor = Actor.objects.prefetch_related('starring_movies').annotate(
        movies_count=Count('starring_movies'),
        avg_rating=Avg('starring_movies__rating')
    ).order_by('-movies_count', 'full_name').first()

    if not actor or not actor.movies_count:
        return ''

    movies = ', '.join(m.title for m in actor.starring_movies.all() if m)

    return (f"Top Actor: {actor.full_name}, starring in movies: {movies}, "
            f"movies average rating: {actor.avg_rating:.1f}")


def get_actors_by_movies_count():
    actors = Actor.objects.annotate(movies_count=Count('actor_movies')).order_by('-movies_count', 'full_name')[:3]
    if not actors or not actors[0].movies_count:
        return ""

    result = []
    for actor in actors:
        result.append(f"{actor.full_name}, participated in {actor.movies_count} movies")

    return "\n".join(result)


def get_top_rated_awarded_movie():
    movie = Movie.objects.filter(is_awarded=True).order_by('-rating', 'title').first()

    if not movie:
        return ""

    # movie = Movie.objects\
    #     .select_related('starring_actor')\
    #     .prefetch_related('actors') \
    #     .filter(is_awarded=True) \
    #     .order_by('-rating', 'title') \
    #     .first()
    #
    # if movie is None:
    #     return ""

    starring_actor = movie.starring_actor.full_name if movie.starring_actor else 'N/A'

    # cast = ', '.join(sorted([actor.full_name for actor in movie.actors.all()]))

    participating_actors = movie.actors.order_by('full_name').values_list('full_name', flat=True)
    cast = ", ".join(participating_actors)

    return (f"Top rated awarded movie: {movie.title}, rating: {movie.rating:.1f}. "
            f"Starring actor: {starring_actor}. Cast: {cast}.")


def increase_rating():
    movies = Movie.objects.filter(is_classic=True, rating__lt=10.0)

    if not movies:
        return "No ratings increased."

    updated_movies_rating = movies.update(rating=Coalesce(F('rating') + 0.1, 10,00))

    return f"Rating increased for {updated_movies_rating} movies."
