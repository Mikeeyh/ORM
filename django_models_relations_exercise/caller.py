import os
from datetime import date, timedelta
import django
from django.db.models import QuerySet, Sum, Count, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


from main_app.models import Author, Book, Artist, Song, Product, Review, DrivingLicense, Driver, Owner, Registration, \
    Car


def show_all_authors_with_their_books():
    result = []
    authors = Author.objects.all().order_by("id")

    for author in authors:
        books = Book.objects.filter(author=author)  # Equals to: books = author.book_set.all()

        if not books:
            continue

        titles = ", ".join(b.title for b in books)

        result.append(f"{author.name} has written - {titles}!")

    return '\n'.join(result)


def delete_all_authors_without_books():
    Author.objects.filter(book__isnull=True).delete()


# # Create authors
# author1 = Author.objects.create(name="J.K. Rowling")
# author2 = Author.objects.create(name="George Orwell")
# author3 = Author.objects.create(name="Harper Lee")
# author4 = Author.objects.create(name="Mark Twain")
#
# # Create books associated with the authors
#
# book1 = Book.objects.create(
#     title="Harry Potter and the Philosopher's Stone",
#     price=19.99,
#     author=author1
# )
#
# book2 = Book.objects.create(
#     title="1984",
#     price=14.99,
#     author=author2
# )
#
# book3 = Book.objects.create(
#     title="To Kill a Mockingbird",
#     price=12.99,
#     author=author3
# )
#
# # Display authors and their books
# authors_with_books = show_all_authors_with_their_books()
# print(authors_with_books)
#
# # Delete authors without books
# delete_all_authors_without_books()
# print(Author.objects.count())


def add_song_to_artist(artist_name: str, song_title: str) -> None:
    artist = Artist.objects.get(name=artist_name)  # SELECT * FROM artist WHERE name = "Eminem"
    song = Song.objects.get(title=song_title)

    artist.songs.add(song)  # remove, clear

    # Artist.objects.get(name=artist_name).songs.add(Song.objects.get(title=song_title))


def get_songs_by_artist(artist_name: str) -> QuerySet[Song]:
    return Artist.objects.get(name=artist_name).songs.all().order_by("-id")


def remove_song_from_artist(artist_name: str, song_title: str) -> None:
    artist = Artist.objects.get(name=artist_name)  # SELECT * FROM artist WHERE name = "Eminem"
    song = Song.objects.get(title=song_title)

    artist.songs.remove(song)
    # song.artists.remove(artist) the same


def calculate_average_rating_for_product_by_name(product_name: str):
    given_product = Product.objects.get(name=product_name)
    average_rating = given_product.reviews.aggregate(Avg('rating'))['rating__avg']
    return average_rating

# OR:

# def calculate_average_rating_for_product_by_name(product_name: str):
#     given_product = Product.objects.get(name=product_name)
#     reviews = given_product.reviews.all()
#
#     total_rating = sum(r.rating for r in reviews)
#     average_rating = total_rating / len(reviews) / len(reviews)
#
#     return average_rating

# OR:

# def calculate_average_rating_for_product_by_name(product_name: str) -> float:#
#     product = Product.objects.annotate(
#         average_rating=Avg('reviews__rating'),
#     ).get(name=product_name)
#
#     return product.average_rating


def get_reviews_with_high_ratings(threshold: int):
    return Review.objects.filter(rating__gte=threshold)


def get_products_with_no_reviews():
    return Product.objects.filter(reviews__isnull=True).order_by("-name")


def delete_products_without_reviews():
    Product.objects.filter(reviews__isnull=True).delete()

    # OR: get_products_with_no_reviews().delete()


# # Create some products
# product1 = Product.objects.create(name="Laptop")
# product2 = Product.objects.create(name="Smartphone")
# product3 = Product.objects.create(name="Headphones")
# product4 = Product.objects.create(name="PlayStation 5")
#
# # Create some reviews for products
# review1 = Review.objects.create(description="Great laptop!", rating=5, product=product1)
# review2 = Review.objects.create(description="The laptop is slow!", rating=2, product=product1)
# review3 = Review.objects.create(description="Awesome smartphone!", rating=5, product=product2)
#
# # Run the function to get products without reviews
# products_without_reviews = get_products_with_no_reviews()
# print(f"Products without reviews: {', '.join([p.name for p in products_without_reviews])}")
#
# # Run the function to delete products without reviews
# delete_products_without_reviews()
# print(f"Products left: {Product.objects.count()}")
#
# # Calculate and print the average rating
# print(calculate_average_rating_for_product_by_name("Laptop"))


def calculate_licenses_expiration_dates():
    licenses = DrivingLicense.objects.order_by("-license_number")

    return "\n".join(str(l) for l in licenses)


def get_drivers_with_expired_licenses(due_date: date):
    expiration_cutoff_date = due_date - timedelta(days=365)  # Taking the interval of the non expired licenses

    drivers_with_expired_licenses = Driver.objects.filter(
        license__issue_date__gt=expiration_cutoff_date,
    )

    return drivers_with_expired_licenses


def register_car_by_owner(owner: Owner):
    registration = Registration.objects.filter(car__isnull=True).first()
    car = Car.objects.filter(registration__isnull=True).first()

    car.owner = owner
    car.registration = registration
    car.save()

    registration.registration_date = date.today()
    registration.car = car

    registration.save()

    return (f"Successfully registered {car.model} to {owner.name} "
            f"with registration number {registration.registration_number}.")
