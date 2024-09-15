from django.contrib import admin

from main_app.models import Director, Actor, Movie


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'birth_date', 'nationality')
    search_fields = ('full_name', 'nationality')
    list_filter = ('years_of_experience',)


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'birth_date', 'nationality')
    search_fields = ('full_name',)
    list_filter = ('is_awarded',)
    readonly_fields = ('last_updated',)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'storyline', 'rating', 'director')
    search_fields = ('title', 'director__full_name')
    list_filter = ('is_awarded', 'is_classic', 'genre')
    readonly_fields = ('last_updated',)
