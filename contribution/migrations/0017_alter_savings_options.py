# Generated by Django 4.2.13 on 2024-05-21 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contribution', '0016_savings_delete_fund_savings_savings_type_67c85d_idx'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='savings',
            options={'ordering': ['-type'], 'verbose_name_plural': 'savings'},
        ),
    ]
