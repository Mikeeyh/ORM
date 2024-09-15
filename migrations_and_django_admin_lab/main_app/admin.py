from django.contrib import admin

from main_app.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    # Display the fields:
    list_display = ('name', 'category', 'price', 'created_on')

    # Enable searching:
    search_fields = ('name', 'category', 'supplier')

    # Create filters
    list_filter = ('category', 'supplier')

    # Control the layout of "Add" and "Change" pages by grouping related fields within different sections:
    fieldsets = (
        # Group:
        ('General Information', {
            'fields': ('name', 'description', 'price', 'barcode')
        }),

        # Group:
        ('Categorization', {
            'fields': ('category', 'supplier')
        }),
    )

    # Enable date-based drill-down navigation by the "created_on" field:
    date_hierarchy = 'created_on'
