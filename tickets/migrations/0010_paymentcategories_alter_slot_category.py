# Generated by Django 4.0.6 on 2022-07-25 09:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0009_event_starting_from_alter_event_available_slots'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=300, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='slot',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tickets.paymentcategories'),
        ),
    ]