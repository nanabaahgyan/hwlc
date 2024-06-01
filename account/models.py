from django.db import models
# from django.conf import settings
from easy_thumbnails.fields import ThumbnailerImageField

# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


# Create your models here.

class UserProfile(models.Model):
    """
    Extend the default User model with extra user of member
    """
    user = models.OneToOneField(get_user_model(),
                                on_delete=models.CASCADE,
                                related_name='user_profile')
    telephone = models.CharField(max_length=50)
    date_of_birth = models.DateField(blank=True,
                                     null=True,
                                     verbose_name="Date of birth (yyyy-mm-dd)")
    photo = ThumbnailerImageField(upload_to='users/%Y/%m/%d/',
                                  null=True,
                                  blank=True,
                                  resize_source=dict(size=(300, 300), sharpen=True))  # type: ignore
    bank_name = models.CharField(blank=True,
                                 null=True)
    bank_acct_no = models.CharField(verbose_name='Bank account no.',
                                    blank=True,
                                    null=True)
    bank_acct_branch = models.CharField(verbose_name='Bank account branch',
                                        blank=True,
                                        null=True)

    def __str__(self):
        return f'Profile of {self.user.first_name} {self.user.last_name}' # type: ignore
