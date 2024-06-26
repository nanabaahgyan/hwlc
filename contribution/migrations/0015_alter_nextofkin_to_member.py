# Generated by Django 4.2.13 on 2024-05-20 19:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contribution', '0014_alter_fund_member_alter_withdrawal_member'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nextofkin',
            name='to_member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_next_of_kin', to=settings.AUTH_USER_MODEL),
        ),
    ]
