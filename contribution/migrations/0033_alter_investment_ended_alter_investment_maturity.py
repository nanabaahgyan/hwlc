# Generated by Django 5.0.6 on 2024-06-01 19:06

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contribution', '0032_remove_investment_member_investment_ended_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment',
            name='ended',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 31, 19, 6, 30, 953286, tzinfo=datetime.timezone.utc), help_text='Day of maturity'),
        ),
        migrations.AlterField(
            model_name='investment',
            name='maturity',
            field=models.IntegerField(default=0, help_text='Maturity type', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
