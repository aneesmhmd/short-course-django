# Generated by Django 4.2.6 on 2023-10-31 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_amount_remove_courses_fee_remove_courses_is_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='is_available',
            field=models.BooleanField(default=False),
        ),
    ]