from django.db import models
# from django.conf import settings
from easy_thumbnails.fields import ThumbnailerImageField

from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class UserProfile(models.Model):
    """
    Extend the default User model with extra user of member
    """
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='user_profile')
    telephone = models.CharField(max_length=50)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = ThumbnailerImageField(upload_to='users/%Y/%m/%d/',
                                  null=True,
                                  blank=True,
                                  resize_source=dict(size=(300, 300), sharpen=True))  # type: ignore

    def __str__(self):
        return f'Profile of {self.user.username}'
