# Generated by Django 4.0.6 on 2022-07-24 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0003_remove_event_venue_remove_venue_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='available_slots',
            field=models.ManyToManyField(blank=True, to='tickets.slot'),
        ),
    ]
