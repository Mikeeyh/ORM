import os
from decimal import Decimal

import django
from django.db.models import F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character


def create_pet(name: str, species: str):
    pet = Pet.objects.create(
        name=name,
        species=species
    )

    return f"{pet.name} is a very cute {pet.species}!"

# Create queries within functions


# print(create_pet('Buddy', 'Dog'))
# print(create_pet('Whiskers', 'Cat'))
# print(create_pet('Rocky', 'Hamster'))


def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool):
    artifact = Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical
    )

    return f"The artifact {artifact.name} is {artifact.age} years old!"


def rename_artifact(artifact: Artifact, new_name: str):
    # Artifact.objects.filter(is_magical=True, age__gt=250, pk=artifact.pk).update(name=new_name)
    if artifact.is_magical and artifact.age > 250:
        artifact.name = new_name
        artifact.save()
        return True
    return False


def delete_all_artifacts():
    Artifact.objects.all().delete()


# print(
#     create_artifact(
#         'Ancient Sword',
#         'Lost Kingdom',
#         500,
#         'A legendary sword with a rich history',
#         True))
# artifact_object = Artifact.objects.get(name='Ancient Sword')
# rename_artifact(artifact_object, 'Ancient Shield')
# print(artifact_object.name)


# def add_locations():
#     locations_data = [
#         {
#             "name": "Sofia",
#             "region": "Sofia Region",
#             "population": 1329000,
#             "description": "The capital of Bulgaria and the largest city in the country",
#             "is_capital": False
#         },
#         {
#             "name": "Plovdiv",
#             "region": "Plovdiv Region",
#             "population": 346942,
#             "description": "The second-largest city in Bulgaria with a rich historical heritage",
#             "is_capital": False
#         },
#         {
#             "name": "Varna",
#             "region": "Varna Region",
#             "population": 330486,
#             "description": "A city known for its sea breeze and beautiful beaches on the Black Sea",
#             "is_capital": False
#         }
#     ]
#
#     for location_data in locations_data:
#         Location.objects.create(**location_data)
#
# # Run the function to add locations
#
#
# add_locations()


def show_all_locations():
    result = []
    locations = Location.objects.all().order_by('-id')

    for location in locations:
        result.append(f"{location.name} has a population of {location.population}!")

    return '\n'.join(result)


def new_capital():
    first_location = Location.objects.first()
    first_location.is_capital = True
    first_location.save()


def get_capitals():
    return Location.objects.all().filter(is_capital=True).values('name')


def delete_first_location():
    Location.objects.first().delete()


# print(show_all_locations())
# print(new_capital())
# print(get_capitals())


# cars_data = [
#     {"model": "Mercedes C63 AMG", "year": 2019, "color": "white", "price": 120000.00},
#     {"model": "Audi Q7 S line", "year": 2023, "color": "black", "price": 183900.00},
#     {"model": "Chevrolet Corvette", "year": 2021, "color": "dark grey", "price": 199999.00},
# ]
#
# # Add cars to the database
# for car_data in cars_data:
#     Car.objects.create(
#         model=car_data["model"],
#         year=car_data["year"],
#         color=car_data["color"],
#         price=car_data["price"],
#         price_with_discount=0
#     )


def apply_discount():
    cars = Car.objects.all()

    for car in cars:
        discount_percentage = sum([int(digit) for digit in str(car.year)])
        car.price_with_discount = car.price * (Decimal(1 - discount_percentage / 100))
        car.save()


def get_recent_cars():
    cars = Car.objects.all().filter(year__gt=2020).values('model', 'price_with_discount')
    return cars


def delete_last_car():
    Car.objects.last().delete()


# apply_discount()
# print(get_recent_cars())


def show_unfinished_tasks():
    result = []
    tasks = Task.objects.all().filter(is_finished=False)

    for task in tasks:
        result.append(f"Task - {task.title} needs to be done until {task.due_date}!")
    return '\n'.join(result)


def complete_odd_tasks():
    tasks = Task.objects.all()

    for task in tasks:
        if task.pk % 2 != 0:
            task.is_finished = True
            task.save()

#   Instead of 'task.save()', we can use: Task.objects.bulk_update(tasks, ['is_finished'])


def encode_and_replace(text: str, task_title: str):
    encoded_text = ''
    tasks = Task.objects.all().filter(title=task_title)

    for char in text:
        encoded_char = chr(ord(char) - 3)
        encoded_text += encoded_char

    for task in tasks:
        task.description = encoded_text
        task.save()


# def encode_and_replace(text: str, task_title: str):
#     decoded_text = ''.join(chr(ord(symbol) - 3) for symbol in text)
#     Task.objects.filter(title=task_title).update(description=decoded_text)


# encode_and_replace("Zdvk#wkh#glvkhv$", "Simple Task")
# print(Task.objects.get(title='Simple Task').description)


def get_deluxe_rooms():
    result = []
    rooms = HotelRoom.objects.all()

    for room in rooms:
        if room.room_type == "Deluxe" and room.pk % 2 == 0:
            result.append(f"Deluxe room with number {room.room_number} costs {room.price_per_night}$ per night!")

    return '\n'.join(result)


# def get_deluxe_rooms():
#     deluxe_rooms = HotelRoom.objects.filter(room_type="Deluxe")
#     even_deluxe_rooms = [str(r) for r in deluxe_rooms if r.id % 2 == 0]
#
#     return '\n'.join(even_deluxe_rooms)

# For this we should have str method in our model:
#  def __str__(self):
#       return f"(self.room_type) with number {self.room_number} costs {self.price_per_night}$ per night!"


def increase_room_capacity():
    rooms = HotelRoom.objects.order_by('id')  # Order rooms by id in ascending order
    previous_capacity = 0

    for room in rooms:
        if room.is_reserved:
            if previous_capacity == 0:
                room.capacity += room.pk
            else:
                room.capacity += previous_capacity
            room.save()
        previous_capacity = room.capacity


def reserve_first_room():
    first_room = HotelRoom.objects.first()
    first_room.is_reserved = True
    first_room.save()


def delete_last_room():
    last_room = HotelRoom.objects.last()
    if not last_room.is_reserved:
        last_room.delete()


def update_characters():
    characters = Character.objects.all()

    for character in characters:
        if character.class_name == "Mage":
            character.level += 3
            character.intelligence -= 7
        elif character.class_name == "Warrior":
            character.hit_points /= 2
            character.dexterity += 4
        else:
            character.inventory = "The inventory is empty"
        character.save()


# def update_characters():
#     Character.objects.filter(class_name="Mage").update(
#         level=F('level') + 3,
#         intelligence=F('intelligence') - 7
#     )
#
#     Character.objects.filter(class_name="Warrior").update(
#         hit_points=F('hit_points') / 2,
#         dexterity=F('dexterity') + 4
#     )
#
#     Character.objects.filter(class_name__in=["Assassin", "Scout"]).update(
#         inventory="The inventory is empty"
#     )

# 'F' gives us the initial amount


def fuse_characters(first_character: Character, second_character: Character):
    name = f"{first_character.name} {second_character.name}"
    class_name = "Fusion"
    level = (first_character.level + second_character.level) // 2
    strength = (first_character.strength + second_character.strength) * 1.2
    dexterity = (first_character.dexterity + second_character.dexterity) * 1.4
    intelligence = (first_character.intelligence + second_character.intelligence) * 1.5
    hit_points = first_character.hit_points + second_character.hit_points
    inventory = ""

    if first_character.class_name in ["Mage", "Scout"]:
        inventory = "Bow of the Elven Lords, Amulet of Eternal Wisdom"
    elif first_character.class_name in ["Warrior", "Assassin"]:
        inventory = "Dragon Scale Armor, Excalibur"

    new_character = Character.objects.create(
        name=name,
        class_name=class_name,
        level=level,
        strength=strength,
        dexterity=dexterity,
        intelligence=intelligence,
        hit_points=hit_points,
        inventory=inventory
    )

    first_character.delete()
    second_character.delete()

    return new_character


def grand_dexterity():
    characters = Character.objects.all()
    for character in characters:
        character.dexterity = 30
        character.save()

    # Character.objects.update(dexterity=30)


def grand_intelligence():
    characters = Character.objects.all()
    for character in characters:
        character.intelligence = 40
        character.save()

    # Character.objects.update(intelligence=40)


def grand_strength():
    characters = Character.objects.all()
    for character in characters:
        character.strength = 50
        character.save()

    # Character.objects.update(strength=50)


def delete_characters():
    characters = Character.objects.all()

    for character in characters:
        if character.inventory == "The inventory is empty":
            character.delete()

    # Character.objects.filter(inventory="The inventory is empty").delete()
