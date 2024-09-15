import os
import django
from django.db.models import Q, Count, Sum, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Astronaut, Spacecraft, Mission


def get_astronauts(search_string=None):
    if search_string is None:
        return ""

    result = []

    astronauts = Astronaut.objects.filter(
        Q(name__icontains=search_string) | Q(phone_number__icontains=search_string)
    ).order_by('name')

    if not astronauts.exists():
        return ""

    for current_astronaut in astronauts:
        status = "Active" if current_astronaut.is_active else "Inactive"
        result.append(f"Astronaut: {current_astronaut.name}, phone number: {current_astronaut.phone_number}, status: {status}")

    return "\n".join(result)


def get_top_astronaut():
    top_astronaut = (Astronaut.objects
                     .annotate(missions_count=Count('missions'))
                     .order_by('-missions_count', 'phone_number')
                     .first()
                     )

    if not top_astronaut or top_astronaut.missions_count == 0:
        return "No data."

    return f"Top Astronaut: {top_astronaut.name} with {top_astronaut.missions_count} missions."


def get_top_commander():
    top_commander = (Astronaut.objects
                     .annotate(commanded_missions_count=Count('commander_missions'))
                     .order_by('-commanded_missions_count', 'phone_number')
                     .first()
                     )

    if not top_commander or top_commander.commanded_missions_count == 0:
        return "No data."

    return f"Top Commander: {top_commander.name} with {top_commander.commanded_missions_count} commanded missions."


def get_last_completed_mission():
    last_completed_mission = Mission.objects.filter(status=Mission.Statuses.COMPLETED).order_by('-launch_date').first()

    if not last_completed_mission:
        return "No data."

    commander = last_completed_mission.commander.name if last_completed_mission.commander else "TBA"

    astronauts = last_completed_mission.astronauts.order_by('name').values_list('name', flat=True)
    astronauts_string = ", ".join(astronauts)

    total_spacewalks = last_completed_mission.astronauts.aggregate(
        total_spacewalks=Sum('spacewalks'))['total_spacewalks'] or 0

    return (f"The last completed mission is: {last_completed_mission.name}. "
            f"Commander: {commander}. "
            f"Astronauts: {astronauts_string}. "
            f"Spacecraft: {last_completed_mission.spacecraft.name}. "
            f"Total spacewalks: {total_spacewalks}.")


def get_most_used_spacecraft():
    if not Mission.objects.exists():
        return "No data."

    most_used_spacecraft = (Spacecraft.objects
                            .annotate(missions_count=Count('mission'))
                            .order_by('-missions_count', 'name')
                            .first()
                            )

    if not most_used_spacecraft or most_used_spacecraft.missions_count == 0:
        return "No data."

    astronauts_count = Astronaut.objects.filter(missions__spacecraft=most_used_spacecraft).distinct().count()

    return (f"The most used spacecraft is: {most_used_spacecraft.name}, "
            f"manufactured by {most_used_spacecraft.manufacturer}, "
            f"used in {most_used_spacecraft.missions_count} missions, "
            f"astronauts on missions: {astronauts_count}.")


def decrease_spacecrafts_weight():
    spacecrafts_to_update = (Spacecraft.objects
                             .filter(mission__status=Mission.Statuses.PLANNED, weight__gte=200.0)
                             .distinct()
                             )

    if not spacecrafts_to_update.exists():
        return "No changes in weight."

    num_spacecrafts_affected = spacecrafts_to_update.update(weight=F('weight') - 200.0)

    if num_spacecrafts_affected == 0:
        return "No changes in weight."

    avg_weight = Spacecraft.objects.aggregate(
        avg_weight=Sum('weight') / Count('id')
    )['avg_weight']

    avg_weight = round(avg_weight, 1)

    return (f"The weight of {num_spacecrafts_affected} spacecrafts has been decreased. "
            f"The new average weight of all spacecrafts is {avg_weight}kg")
