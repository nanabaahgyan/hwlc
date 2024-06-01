from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from easy_thumbnails.fields import ThumbnailerImageField
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

import datetime
import uuid
from decimal import Decimal


# Create your models here.
class Type(models.TextChoices):
    HEALTH = 'HF', 'Health Fund'
    PENSION = 'PF', 'Pension Fund'


class Savings(models.Model):

    narration = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=8,
                                 decimal_places=2,
                                 validators=[MinValueValidator(Decimal('0.00'))])
    member = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='member_savings')
    created = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=2,
                            choices=Type.choices,
                            default=Type.HEALTH)

    class Meta:
        db_table = 'savings'
        verbose_name_plural = "savings"
        ordering = ['-type']
        indexes = [
            models.Index(fields=['-type']),
        ]

    def get_absolute_url(self):
        return reverse('savings-detail',
                       kwargs={"member": self.member})

    def __str__(self) -> str:
        return f"Contribution of {self.amount}"


class Withdrawal(models.Model):

    narration = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=7,
                                 decimal_places=2,
                                 validators=[MinValueValidator(Decimal('0.00'))])
    member = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='member_withdrawal')
    withdrawn = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=2,
                            choices=Type.choices,
                            default=Type.HEALTH)

    class Meta:
        db_table = 'withdrawal'

    def get_absolute_url(self):
        return reverse("withdrawal-detail",
                       kwargs={"pk": self.pk})

    def clean(self, *args, **kwargs):
        super(Withdrawal, self).clean(*args, **kwargs)

        # get total savings from db
        total_savings = Savings.objects.all()\
            .filter(member=self.member.id)\
            .filter(type=self.type)\
            .aggregate(Sum('amount'))
        total_savings = total_savings.get("amount__sum")

        # if member has no savings yet they cannot withdraw money
        if total_savings is None:
            raise ValidationError(
                {"amount": _(
                    f"No savings yet for {self.member.first_name}\
                          {self.member.last_name} on {self.type} account.")
                 }
            )

        # get total withdrawals from db
        total_withdrawals = self.__class__._default_manager\
            .filter(member=self.member.id)\
            .filter(type=self.type)\
            .aggregate(Sum('amount'))
        total_withdrawals = total_withdrawals.get("amount__sum")

        # if this is a new withdrawal make None a 0
        if total_withdrawals is None:
            new_total_withdrawals = Decimal('0') + self.amount
        else:
            # add previous withdrawals to new one for a new total
            new_total_withdrawals = total_withdrawals + self.amount

        # check if they have enough money to withdraw. otherwise raise an error.
        if not None and Decimal(new_total_withdrawals) > Decimal(total_savings):
            raise ValidationError(
                {"amount": _(
                    f"{self.amount} is bigger than the total savings of {self.member.first_name} {self.member.last_name} on {self.type} account.")
                 }
            )

    def __str__(self) -> str:
        return f"Withdrawal of {self.amount}"


class Investment(models.Model):
    narration = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10,
                                 decimal_places=2,
                                 help_text="Amount invested",
                                 validators=[MinValueValidator(Decimal('0.00'))])
    maturity = models.IntegerField(default=0,
                                   help_text="Maturity type",
                                   validators=[MinValueValidator(0),
                                               MaxValueValidator(100)])
    is_active = models.BooleanField(default=True,
                                    help_text="Is this investment still active?")
    rate = models.DecimalField(max_digits=5,
                               decimal_places=2,
                               help_text="Rate at the time of transaction",
                               validators=[MinValueValidator(Decimal('0.00'))])
    members = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     related_name='investments_made',
                                     verbose_name='contributors',
                                     blank=True)
    interest = models.DecimalField(blank=True,
                                   null=True,
                                   max_digits=10,
                                   decimal_places=2,
                                   help_text="Interest earned on investment",
                                   validators=[MinValueValidator(Decimal(0.00))])
    created = models.DateTimeField(default=timezone.now,
                                   help_text="Start of transaction")
    ended = models.DateTimeField(default=timezone.now() + datetime.timedelta(days=91),
                                 help_text="Day of maturity")
    trader = models.CharField(max_length=50)

    class Meta:
        ordering = ['-created']
        db_table = 'investment'

    def __str__(self) -> str:
        return f"Investment of {self.amount}"


class NextOfKin(models.Model):
    class Sex(models.TextChoices):
        Male = 'M', 'Male'
        Female = 'F', 'Female'

    first_name = models.CharField(verbose_name="First Name",
                                  #   blank=False,
                                  #   null=False,
                                  max_length=50)
    last_name = models.CharField(verbose_name="Last Name",
                                 blank=False,
                                 null=False,
                                 max_length=50)
    sex = models.CharField(verbose_name="Sex",
                           blank=False,
                           null=False,
                           max_length=1,
                           choices=Sex.choices,
                           default=Sex.Male)
    telephone = models.CharField(blank=False,
                                 null=False,
                                 max_length=50)
    address = models.TextField(null=False,
                               max_length=150,
                               blank=True)
    city = models.CharField(max_length=20,
                            null=False,
                            blank=True)
    perc = models.DecimalField(verbose_name="Percentage",
                               max_digits=4,
                               decimal_places=1,
                               validators=[MinValueValidator(Decimal('0.0'))])
    country = models.CharField(max_length=20,
                               null=True,
                               blank=True)
    photo = ThumbnailerImageField(upload_to='kins/%Y/%m/%d',
                                  null=True,
                                  blank=True,
                                  resize_source=dict(size=(300, 300), sharpen=True))  # type: ignore
    to_member = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.CASCADE,
                                  related_name='user_next_of_kin')
    uuid = models.UUIDField(primary_key=False,
                            default=uuid.uuid4,
                            editable=False)

    class Meta:
        db_table = 'nextofkin'
        ordering = ['-perc']

    def get_absolute_url(self):
        return reverse('next-of-kin', kwargs={"pk": self.pk})

    @property
    def get_photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        else:
            return None

    def clean(self, *args, **kwargs):
        """Use generic method to validate percentage field"""
        super(NextOfKin, self).clean(*args, **kwargs)

        # if next of kin exists validate assigned percentage
        if NextOfKin.objects.filter(to_member=self.to_member.pk).exists():

            # get total member percentage. exclude already existing value
            total_perc = NextOfKin.objects\
                .filter(to_member=self.to_member.pk)\
                .exclude(id=self.pk)\
                .aggregate(Sum('perc'))
            total_perc = total_perc.get('perc__sum')
        else:
            # a new entry
            total_perc = NextOfKin.objects\
                .filter(to_member=self.to_member.pk)\
                .aggregate(Sum('perc'))
            total_perc = total_perc.get('perc__sum')
        # make None results 0
        if total_perc is None:
            total_perc = 0

        # calculate new total
        new_total_perc = total_perc + self.perc  # type: ignore

        # maximum percentage is 100. raise error if more
        if 100 - new_total_perc < 0:
            raise ValidationError(
                {"perc": _(
                    f"{self.perc} makes total percentage of your\
                        beneficiaries greater than 100.")}
            )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
