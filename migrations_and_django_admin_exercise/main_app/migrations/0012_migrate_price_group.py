from django.db import migrations


def set_price_group(apps, schema_editor):
    item_model = apps.get_model('main_app', 'Item')  # taking our app name (main_app) and our model name (Item)

    items = item_model.objects.all()

    for item in items:
        if item.price <= 10:
            item.rarity = "Rare"
        elif 11 <= item.price <= 20:
            item.rarity = "Very Rare"
        elif 21 <= item.price <= 30:
            item.rarity = "Extremely Rare"
        else:
            item.rarity = "Mega Rare"

    item_model.objects.bulk_update(items, ['rarity'])
    # We can replace this line with item.save() but this will save record by record, so it is slow.


def set_price_group_default(apps, schema_editor):
    item_model = apps.get_model('main_app', 'Item')

    for item in item_model.objects.all():
        item.age_group = item_model._meta.get_field('rarity').default
        # This is equal to: item.rarity = "No rarity", But we take it dynamically.

        item.save()  # could be better


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0011_item'),
    ]

    operations = [
        migrations.RunPython(set_price_group, set_price_group_default)
    ]
