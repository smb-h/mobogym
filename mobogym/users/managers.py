from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import UserManager as AbstractUserManager


# User queryset
class UserQuerySet(models.query.QuerySet):
    def search(self, query):
        if query:
            query = query.strip()
            qs = self.filter(
                    Q(username__icontains=query) |
                    Q(email__icontains=query) |
                    Q(phone__icontains=query) |
                    Q(first_name__icontains=query) |
                    Q(last_name__icontains=query)
                ).distinct()
            return qs
        return self


#  User manager
class UserManager(AbstractUserManager):
    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)

    def get_by_natural_key(self, username):
        return self.get(
            Q(**{self.model.USERNAME_FIELD: username}) |
            Q(**{self.model.EMAIL_FIELD: username}) |
            Q(phone__iexact = username)
        )





