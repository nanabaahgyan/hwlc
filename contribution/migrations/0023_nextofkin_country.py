# Generated by Django 4.2.13 on 2024-05-24 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contribution', '0022_nextofkin_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='nextofkin',
            name='country',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
