from django.urls import path, include
from users.api.views import (
                                UserCreateAPIView,
                                UserRUDAPIView,
                                UserLoginAPIView,
                                UserLogoutAPIView,
                                GroupListAPIView,
                                UserInfoRUAPIView,
                                UserCheckEmailView
                            )
# JWT
# from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token



urlpatterns = [

    # User
    path('Sign_up', UserCreateAPIView.as_view(), name='user_create_api'),
    path('Sign_in', UserLoginAPIView.as_view(), name='user_login_api'),
    path('Sign_out', UserLogoutAPIView.as_view(), name='user_logout_api'),
    path('Info', UserInfoRUAPIView.as_view(), name='user_info_api'),
    path('Chech-email', UserCheckEmailView.as_view(), name='user_check_email_api'),
    # Group
    path('Groups/', GroupListAPIView.as_view(), name='group_list_api'),
    # JWT
    # path('Token/', obtain_jwt_token),
    # path('Token/Refresh', refresh_jwt_token),
    # path('Token/Verify', verify_jwt_token),
    # User
    path('<username>', UserRUDAPIView.as_view(), name='user_rud_api'),
]
