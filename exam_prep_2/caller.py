import os
import django
from django.db.models import Q, Count, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Profile, Product, Order


def get_profiles(search_string=None) -> str:
    if search_string is None:
        return ""

    profiles = Profile.objects.filter(
        Q(full_name__icontains=search_string)
            |
        Q(email__icontains=search_string)
            |
        Q(phone_number__icontains=search_string)
    ).order_by('full_name')

    if not profiles.exists():
        return ""

    return "\n".join(
        f"Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, orders: {p.orders.count()}"
        for p in profiles
    )


def get_loyal_profiles():
    loyal_profiles = Profile.objects.get_regular_customers()
    result = []
    for p in loyal_profiles:
        result.append(f"Profile: {p.full_name}, orders: {p.num_orders}")
    return '\n'.join(result) if result else ""


def get_last_sold_products():
    last_order = Order.objects.prefetch_related("products").last()
    if last_order is None or not last_order.products.exists():
        return ""
    last_sold_products = last_order.products.all().order_by('name')

    last_sold_products_str = ", ".join(product.name for product in last_sold_products)
    return f"Last sold products: {last_sold_products_str}"

# def get_last_sold_products() -> str:
#     last_order = Order.objects.prefetch_related('products').last()
#
#     if last_order is None or not last_order.products.exists():
#         return ""
#
#     # products = ', '.join([p.name for p in last_order.products.order_by('name')])
#     products = ', '.join(last_order.products.order_by('name').values_list('name', flat=True))
#
#     return f"Last sold products: {products}"

# def get_last_sold_products():
#     try:
#         last_order = Order.objects.prefetch_related('products').latest('creation_date')
#         last_sold_products = last_order.products.all().order_by('name')
#
#         if last_sold_products:
#             last_sold_products_str = ", ".join(product.name for product in last_sold_products)
#             return f"Last sold products: {last_sold_products_str}"
#         return ""
#     except Order.DoesNotExist:
#         return ""


def get_top_products():
    top_products = (Product.objects
                    .annotate(num_orders=Count('order'))
                    .filter(num_orders__gt=0)
                    .order_by('-num_orders', 'name')[:5])

    if not top_products:
        return ""

    top_products_str = "\n".join(f"{product.name}, sold {product.num_orders} times" for product in top_products)
    return f"Top products:\n{top_products_str}"


def apply_discounts():
    updated_orders = (Order.objects
                      .annotate(products_count=Count('products'))
                      .filter(Q(products_count__gt=2) & Q(is_completed=False))
                      .update(total_price=F('total_price') * 0.9)
                      )

    return f"Discount applied to {updated_orders} orders."


def complete_order():
    oldest_order = Order.objects.filter(is_completed=False).order_by('creation_date').first()

    if not oldest_order:
        return ""

    oldest_order.is_completed = True
    oldest_order.save()

    for product in oldest_order.products.all():
        product.in_stock -= 1
        if product.in_stock <= 0:
            product.in_stock = 0
            product.is_available = False
        product.save()

    return "Order has been completed!"

