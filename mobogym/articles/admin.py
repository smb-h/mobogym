from django.contrib import admin
from articles.models import Article
from app.utils.Timetable import get_read_time
from django import forms
from django_jalali.admin.filters import JDateFieldListFilter
# Ckeditor
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor.widgets import CKEditorWidget


class ArticleAdminForm(forms.ModelForm):
    class Meta:
        model = Article
        localized_fields = ('publish',)
        fields = "__all__"

        # https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#overriding-the-default-fields
        # widgets = {
        #     'content': CKEditorUploadingWidget(config_name='ck_blog'),
        #     'summary': CKEditorWidget(config_name='ck_comment'),
        # }


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    fieldsets = [
        ('Article', {'fields': ['title', 'image', 'content', 'summary', 'attach',]}),
        # ('Date information', {'fields': ['publish'],
        # 'classes': ['collapse']}),
        # ('Date & time', {'fields': ['status', 'publish',]}),
    ]

    readonly_fields = ('updated', 'author', 'read_time', 'created', 'id', 'slug')
    list_display = ('title', 'publish', 'was_published_recently', 'author', 'updated')
    list_filter = (('publish', JDateFieldListFilter), 'author')
    # filter_horizontal = ("tags", "aliases", "keywords")
    # raw_id_fields = ("process",)
    # date_hierarchy = 'publish'
    # prepopulated_fields = {"slug": ("title",)}
    search_fields = ('title', 'author__first_name', 'author__last_name', 'content',)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.read_time = get_read_time(obj.content)
        super().save_model(request, obj, form, change)




