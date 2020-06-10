from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from rest_framework.reverse import reverse as api_reverse
from users.managers import UserManager
import uuid
import datetime
from django.utils import timezone
from django_jalali.db import models as jmodels
from django.contrib.contenttypes.fields import GenericRelation



# user media directories
def user_upload_path(self, filename):
    # file will be uploaded to MEDIA_ROOT/username/
    return("{0}/{1}".format(self, filename))


# User
class User(AbstractUser):

    # OverWrite base email field
    email = models.EmailField(_('Email Address'), blank = True, null = True)
    phone = models.CharField(_('Phone Number'), blank = True, null = True, max_length = 16)
    birth_date = models.DateField(_('Birth Date'), blank = True, null = True)
    image = models.ImageField(upload_to = user_upload_path, verbose_name=_("Image"), null=True, blank=True)
    # date_joined = jmodels.jDateTimeField(auto_now_add = True, auto_now = False, verbose_name = _('Created'))
    # last_login = jmodels.jDateTimeField(auto_now_add = False, auto_now = True, verbose_name = _('Last login'))

    objects = UserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-date_joined']


    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.id})

    def get_api_url(self, request = None):
        return api_reverse('users:user_detail_api', kwargs={"id": self.id}, request = request)

    # OverRiding Save Method
    # https://docs.djangoproject.com/en/2.1/topics/db/models/#overriding-predefined-model-methods
    def save(self, *args, **kwargs):
        # Send Activation mail
        # Call the "real" save() method.
        super().save(*args, **kwargs)
        # do_something_else()




