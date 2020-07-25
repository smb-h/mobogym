from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from users.forms import UserChangeForm, UserCreationForm
from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin

User = get_user_model()


# User admin
@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("image", "phone", "birth_date", "age", "gender",)}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "phone", "birth_date", "last_login", "is_superuser"]
    search_fields = ["name"]
    list_filter = (
        ('date_joined', JDateFieldListFilter),
    )
    readonly_fields = ["date_joined", "id", "last_login"]



