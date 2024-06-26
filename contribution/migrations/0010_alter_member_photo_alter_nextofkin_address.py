# Generated by Django 4.2.13 on 2024-05-18 17:28

from django.db import migrations, models
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contribution', '0009_alter_member_photo_alter_nextofkin_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='photo',
            field=easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, upload_to='contribution'),
        ),
        migrations.AlterField(
            model_name='nextofkin',
            name='address',
            field=models.TextField(blank=True, max_length=150),
        ),
    ]
