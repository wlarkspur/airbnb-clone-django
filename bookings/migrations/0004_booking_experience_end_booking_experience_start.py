# Generated by Django 4.2.3 on 2023-09-02 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0003_alter_booking_experience_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='experience_end',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='experience_start',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
