from django.db import models
from django.db.models import Q


# Article queryset
class ArticleQuerySet(models.query.QuerySet):
    # Search
    def search(self, query):
        if query:
            query = query.strip()
            qs = self.filter(
                                Q(title__icontains=query) |
                                Q(content__icontains=query) |
                                Q(summary__icontains=query) |
                                Q(auther__first_name__icontains=query) |
                                Q(auther__last_name__icontains=query)
                ).distinct()
            return qs
        return self


# Article manager
class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)

    # def all(self):
    #     return super(ServicesCategoryManager , self).all()

