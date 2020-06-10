from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from django.urls import include, path
# from mobogym.users.api.views import UserViewSet
from mobogym.users.api.views import UserCreateAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)    
from articles.api.views import (
    ArticleList,
    ArticletDetail
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# router.register("users", UserViewSet)


app_name = "API"



urlpatterns = [
    # Router
    path('', include(router.urls)),
    # Accounts
    path('accounts/sign-up', UserCreateAPIView.as_view(), name='sign-up'),
    # Token
    path('accounts/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('accounts/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('accounts/token/verify', TokenVerifyView.as_view(), name='token_verify'),
    # Articles
    path('articles', ArticleList.as_view(), name='articles'),
    path('articles/<id>', ArticletDetail.as_view(), name='article_detail'),
]


