# Generated by Django 4.2.3 on 2023-09-02 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0002_alter_booking_experience_alter_booking_room_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='experience_time',
            field=models.DateField(blank=True, null=True),
        ),
    ]
