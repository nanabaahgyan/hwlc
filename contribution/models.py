from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse

# Create your models here.


class PensionFundManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset()\
                      .filter(type=Savings.Type.PENSION)


class HealthFundManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset()\
                      .filter(type=Savings.Type.HEALTH)


class Savings(models.Model):

    class Type(models.TextChoices):
        HEALTH = 'HF', 'Health Fund'
        PENSION = 'PF', 'Pension Fund'

    narration = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=7,
                                 decimal_places=2)
    member = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='member_savings')
    created = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=2,
                            choices=Type.choices,
                            default=Type.HEALTH)
    objects = models.Manager()
    health_obj = HealthFundManager()
    pension_obj = PensionFundManager()

    class Meta:
        db_table = 'savings'
        verbose_name_plural = "savings"
        ordering = ['-type']
        indexes = [
            models.Index(fields=['-type']),
        ]

    def get_absolute_url(self):
        return reverse('contribution:health_contribution',
                       args=[self.member])

    def __str__(self) -> str:
        return f"Savings for {self.member.first_name + ' ' + self.member.last_name}"


class NextOfKin(models.Model):
    first_name = models.CharField(verbose_name="First Name",
                                  blank=False,
                                  null=False,
                                  max_length=50)
    last_name = models.CharField(verbose_name="Last Name",
                                 blank=False,
                                 null=False,
                                 max_length=50)
    telephone = models.CharField(blank=False,
                                 null=False,
                                 max_length=50)
    address = models.TextField(null=False,
                               max_length=150,
                               blank=True)
    city = models.CharField(max_length=20,
                            null=False,
                            blank=True)
    perc = models.CharField(verbose_name="Percentage",
                            blank=False,
                            null=False,
                            max_length=3)
    to_member = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  related_name='user_next_of_kin')

    def __str__(self):
        return f'Next of kin: {self.first_name + "" + self.last_name}'


class Withdrawal(models.Model):

    class Type(models.TextChoices):
        HEALTH = 'HF', 'Health Fund'
        PENSION = 'PF', 'Pension Fund'

    narration = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    member = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='member_withdrawal')
    when = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=2,
                            choices=Type.choices,
                            default=Type.HEALTH)

    class Meta:
        db_table = 'withdrawal'

    def __str__(self) -> str:
        return f"Withdrawal for {self.member.first_name + '' + self.member.last_name}"
