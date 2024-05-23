# Generated by Django 4.2.13 on 2024-05-23 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contribution', '0019_nextofkin_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='nextofkin',
            name='sex',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='M', max_length=1, verbose_name='Sex'),
        ),
    ]
