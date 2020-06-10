from django.db import models
from django.utils.translation import ugettext_lazy as _
from time import strftime
from django.urls import reverse
from django.conf import settings
import datetime
from django.utils import timezone
from django.db.models import Q
from app.utils.Unique_Slug_Generator import unique_slug_generator
from app.utils.Timetable import get_read_time
from articles.managers import ArticleManager
# from tags.models import Tag, MetaTag, Alias, Keyword
from django_jalali.db import models as jmodels
from rest_framework.reverse import reverse as api_reverse


User = settings.AUTH_USER_MODEL


# initial a directory for files of each user
def upload_path(self, filename):
    # file will be uploaded to MEDIA_ROOT/year-month-day/UserName/FileName
    # return ('Uploads/{0}/{1}/{2}'.format(strftime('%Y-%m-%d'), self.author, filename))
    return ('{0}/{1}'.format(self.author, filename))


# Articles
class Article(models.Model):

    # status
    class StatusChoices(models.TextChoices):
        DELETE = 'delete', _('delete')
        DRAFT = 'draft', _('draft')
        PUBLISH = "publish", _("publish")


    title = models.CharField(max_length = 255, verbose_name = _('Title'))
    image = models.ImageField(blank = True, null = True, upload_to = upload_path, verbose_name = _('Image'))
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = _('Author'))
    content = models.TextField(verbose_name = _('Content'))
    summary = models.CharField(max_length = 511, blank = True, null = True, verbose_name = _('Summery'))
    attach = models.FileField(blank = True, null = True, upload_to = upload_path, verbose_name = _('Attach'))
    # Date Time Information
    created = jmodels.jDateField(auto_now_add = True, auto_now = False, verbose_name = _('Created'))
    updated = jmodels.jDateField(auto_now_add = False, auto_now = True, verbose_name = _('Updated'))
    read_time = models.CharField(max_length = 255, blank = True, null = True, verbose_name = _('Time to read'))
    status = models.CharField(max_length = 32, choices = StatusChoices.choices, default = StatusChoices.DRAFT, verbose_name = _("Status"))
    publish = jmodels.jDateField(blank = True, null = True, verbose_name = _('Publish'))
    # Utils
    slug = models.SlugField(allow_unicode = True, unique = True, verbose_name = _('Slug'))

    objects = ArticleManager()

    def was_published_recently(self):
        if self.publish:
            now = timezone.now()
            return (self.publish <= now and self.status == "publish")
        return None

    was_published_recently.admin_order_field = _('publish')
    was_published_recently.boolean = True
    was_published_recently.short_description = _('published')


    def get_absolute_url(self):
        return reverse('Articles:post', kwargs={"slug": self.slug})

    def get_api_url(self, request = None):
        return api_reverse('API:article_detail_api', kwargs={"id": self.id}, request = request)


    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')
        ordering = ['-publish', 'title']
        # unique_together = ("title", "slug")


    # formatting post objects to show
    def __str__(self):
        return '{} - {}'.format(self.title, self.created)


    # OverRiding Save Method
    # https://docs.djangoproject.com/en/2.1/topics/db/models/#overriding-predefined-model-methods
    def save(self, *args, **kwargs):
        self.slug = unique_slug_generator(self)
        self.read_time = get_read_time(self.content)

        # Call the "real" save() method.
        super().save(*args, **kwargs)
        # do_something_else()


