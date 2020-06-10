from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from rest_framework.permissions import (
                                            AllowAny,
                                            IsAuthenticated,
                                            IsAdminUser,
                                            IsAuthenticatedOrReadOnly
                                        )
from app.api.permissions import IsOwnerOrReadOnly
from users.api.permissions import IsUserOrReadOnly
# OAuth 2
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from users.api.serializers import (
                            UserCreateSerializer,
                            UserDetailSerializer,
                            UserLoginSerializer,
                            GroupSerializer,
                            UserResetPasswordSerializer,
                            UserVerificationSerializer,
                            UserVerificationCheckSerializer
                        )
from django.contrib.auth import authenticate, login, logout
from app.api.pagination import PostPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
# from otps.models import OTP
# from sms.models import SMS
# from otps.api.serializers import OTPVerifySerializer
from django.db.models import Avg, Max, Min
from django.shortcuts import get_object_or_404
# from emails.models import Email
from django.utils.translation import ugettext_lazy as _
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser, JSONParser
import json

User = get_user_model()


# User Create API View
class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    # Create eco user
    # def perform_create(self, serializer):
    #     serializer.save()
    #     eco_user = EcoUser()
    #     user_obj = User.objects.filter(phone = serializer.data["phone"]).distinct().first() 
    #     eco_user.user = user_obj
    #     eco_user.save()
    #     # Send activation code
    #     otp_code = OTP(user = user_obj)
    #     otp_code.save()


# User Activation API View
# class UserActivationAPIView(APIView):
#     permission_classes = [AllowAny]
#     serializer_class = OTPVerifySerializer

#     # Post
#     def post(self, request, *args, **kwargs):
#         data = request.data
#         serializer = OTPVerifySerializer(data = data)
#         if serializer.is_valid(raise_exception = True):
#             data = serializer.data
#             identity = data.get('identity')

#             user = User.objects.filter(
#                 Q(username = identity) |
#                 Q(email = identity) |
#                 Q(phone = identity)
#             ).distinct()

#             user_obj = user.first()
#             user_obj.is_active = True
#             user_obj.save()

#             return Response(data, status = HTTP_200_OK)

#         return Response(serializer.errors, status = HTTP_400_BAD_REQUEST)


# User Retrieve Update Destroy API View
class UserRUDAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [IsUserOrReadOnly, IsAdminUser]
    lookup_field = 'username'

    def get_serializer_context(self, *args, **kwargs):
        context = {'request': self.request}
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = User.objects.filter(username = self.kwargs['username'])
        return queryset


# User Login API View
class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data = data)
        if serializer.is_valid(raise_exception = True):
            new_data = serializer.data

            # https://docs.djangoproject.com/en/dev/topics/auth/default/#how-to-log-a-user-in
            user_auth = authenticate(username = data.get('ID'), password = data.get('password'))
            if user_auth is not None:
                login(request, user_auth)

            return Response(new_data, status = HTTP_200_OK)

        return Response(serializer.errors, status = HTTP_400_BAD_REQUEST)


# User Logout API View
class UserLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserLoginSerializer

    def get(self, request, *args, **kwargs):
        # https://docs.djangoproject.com/en/dev/topics/auth/default/#how-to-log-a-user-out
        logout(request)
        # Redirect to a success page.
        return Response(status = HTTP_200_OK)


# User Reset Password API View
# class UserResetPasswordAPIView(APIView):
#     permission_classes = [AllowAny]
#     serializer_class = UserResetPasswordSerializer

#     # POST
#     def post(self, request, *args, **kwargs):
#         data = request.data
#         serializer = UserResetPasswordSerializer(data = data)
#         if serializer.is_valid(raise_exception = True):
#             # new_data = serializer.data
#             new_data = {"msg": _("Password was changed successfully!")}
#             # https://docs.djangoproject.com/en/dev/topics/auth/default/#changing-passwords
#             identity = data.get('identity')
#             code = data.get('code')
#             new_password = data.get('new_password')
#             user = User.objects.filter(
#                 Q(username = identity) |
#                 Q(email = identity) |
#                 Q(phone = identity)
#             ).distinct().first()

#             user_code = user.codes.filter(code = code, used = False).distinct().first()
#             user_code.used = True
#             user_code.save()

#             user.set_password(new_password)
#             user.save()

#             return Response(new_data, status = HTTP_200_OK)

#         return Response(serializer.errors, status = HTTP_400_BAD_REQUEST)


# Group List API View
class GroupListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter,)
    search_fields = ('title',)
    ordering_fields = ('updated', 'timestamp')



# User Verification API View
# class UserVerificationAPIView(APIView):
#     permission_classes = [AllowAny]
#     serializer_class = UserVerificationSerializer

#     def post(self, request, *args, **kwargs):
#         data = request.data
#         serializer = UserVerificationSerializer(data = data)
#         if serializer.is_valid(raise_exception = True):
#             # new_data = serializer.data
#             new_data = {"msg": _("The authentication code was sent to you.")}
#             # https://docs.djangoproject.com/en/dev/topics/auth/default/#changing-passwords
#             identity = data.get('identity')
#             user = User.objects.filter(
#                 Q(username = identity) |
#                 Q(email = identity) |
#                 Q(phone = identity)
#             ).distinct().first()
#             # SEND RESET CODE
#             code_obj = OTP(user = user)
#             OTP.save(code_obj)

#             # send  email
#             html_result_1 = """
#             <!doctype html>
#             <html>
#             <head>
#                 <meta name="viewport" content="width=device-width">
#                 <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
#                 <title>Simple Transactional Email</title>
#                 <style>
#                 /* -------------------------------------
#                     INLINED WITH htmlemail.io/inline
#                 ------------------------------------- */
#                 /* -------------------------------------
#                     RESPONSIVE AND MOBILE FRIENDLY STYLES
#                 ------------------------------------- */
#                 @media only screen and (max-width: 620px) {
#                 table[class=body] h1 {
#                     font-size: 28px !important;
#                     margin-bottom: 10px !important;
#                 }
#                 table[class=body] p,
#                         table[class=body] ul,
#                         table[class=body] ol,
#                         table[class=body] td,
#                         table[class=body] span,
#                         table[class=body] a {
#                     font-size: 16px !important;
#                 }
#                 table[class=body] .wrapper,
#                         table[class=body] .article {
#                     padding: 10px !important;
#                 }
#                 table[class=body] .content {
#                     padding: 0 !important;
#                 }
#                 table[class=body] .container {
#                     padding: 0 !important;
#                     width: 100% !important;
#                 }
#                 table[class=body] .main {
#                     border-left-width: 0 !important;
#                     border-radius: 0 !important;
#                     border-right-width: 0 !important;
#                 }
#                 table[class=body] .btn table {
#                     width: 100% !important;
#                 }
#                 table[class=body] .btn a {
#                     width: 100% !important;
#                 }
#                 table[class=body] .img-responsive {
#                     height: auto !important;
#                     max-width: 100% !important;
#                     width: auto !important;
#                 }
#                 }

#                 /* -------------------------------------
#                     PRESERVE THESE STYLES IN THE HEAD
#                 ------------------------------------- */
#                 @media all {
#                 .ExternalClass {
#                     width: 100%;
#                 }
#                 .ExternalClass,
#                         .ExternalClass p,
#                         .ExternalClass span,
#                         .ExternalClass font,
#                         .ExternalClass td,
#                         .ExternalClass div {
#                     line-height: 100%;
#                 }
#                 .apple-link a {
#                     color: inherit !important;
#                     font-family: inherit !important;
#                     font-size: inherit !important;
#                     font-weight: inherit !important;
#                     line-height: inherit !important;
#                     text-decoration: none !important;
#                 }
#                 #MessageViewBody a {
#                     color: inherit;
#                     text-decoration: none;
#                     font-size: inherit;
#                     font-family: inherit;
#                     font-weight: inherit;
#                     line-height: inherit;
#                 }
#                 .btn-primary table td:hover {
#                     background-color: #34495e !important;
#                 }
#                 .btn-primary a:hover {
#                     background-color: #34495e !important;
#                     border-color: #34495e !important;
#                 }
#                 }
#                 </style>
#             </head>
#             <body class="" style="text-align: right; direction: rtl; background-color: #f6f6f6; font-family: sans-serif; -webkit-font-smoothing: antialiased; font-size: 14px; line-height: 1.4; margin: 0; padding: 0; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;">
#                 <table border="0" cellpadding="0" cellspacing="0" class="body" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%; background-color: #f6f6f6;">
#                 <tr>
#                     <td style="font-family: sans-serif; font-size: 14px; vertical-align: top;">&nbsp;</td>
#                     <td class="container" style="font-family: sans-serif; font-size: 14px; vertical-align: top; display: block; Margin: 0 auto; max-width: 580px; padding: 10px; width: 580px;">
#                     <div class="content" style="box-sizing: border-box; display: block; Margin: 0 auto; max-width: 580px; padding: 10px;">

#                         <!-- START CENTERED WHITE CONTAINER -->
#                         <span class="preheader" style="color: transparent; display: none; height: 0; max-height: 0; max-width: 0; opacity: 0; overflow: hidden; mso-hide: all; visibility: hidden; width: 0;">This is preheader text. Some clients will show this text as a preview.</span>
#                         <table class="main" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%; background: #ffffff; border-radius: 3px;">

#                         <!-- START MAIN CONTENT AREA -->
#                         <tr>
#                             <td class="wrapper" style="font-family: sans-serif; font-size: 14px; vertical-align: top; box-sizing: border-box; padding: 20px;">
#                             <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%;">
#                                 <tr>
#                                 <td style="font-family: sans-serif; font-size: 14px; vertical-align: top;">
#             """
#             title_html = '<p style="font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; Margin-bottom: 15px;"> کد تایید: <br />' + str(code_obj.code) + '</p><br />'
#             content_html = '<p style="font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; Margin-bottom: 15px;"> این کد به مدت ۵ دقیقه فعال میباشد. </p>'
#             call_to_action_html = """
#             <table border="0" cellpadding="0" cellspacing="0" class="btn btn-primary" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%; box-sizing: border-box;">
#                 <tbody>
#                     <tr>
#                     <td align="left" style="font-family: sans-serif; font-size: 14px; vertical-align: top; padding-bottom: 15px;">
#                         <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: auto;">
#                         <tbody>
#                             <tr>
#                             <td style="font-family: sans-serif; font-size: 14px; vertical-align: top; background-color: #3498db; border-radius: 5px; text-align: center;"> <a href="https://dr.tabaye.ir/" target="_blank" style="display: inline-block; color: #ffffff; background-color: #3498db; border: solid 1px #3498db; border-radius: 5px; box-sizing: border-box; cursor: pointer; text-decoration: none; font-size: 14px; font-weight: bold; margin: 0; padding: 12px 25px; text-transform: capitalize; border-color: #3498db;">طبایع</a> </td>
#                             </tr>
#                         </tbody>
#                         </table>
#                     </td>
#                     </tr>
#                 </tbody>
#             </table>
#             """
#             html_result_2 = """
#                                     </td>
#                                 </tr>
#                             </table>
#                             </td>
#                         </tr>

#                         <!-- END MAIN CONTENT AREA -->
#                         </table>

#                         <!-- START FOOTER -->
#                         <div class="footer" style="clear: both; Margin-top: 10px; text-align: center; width: 100%;">
#                         <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%;">
#                             <tr>
#                             <td class="content-block powered-by" style="font-family: sans-serif; vertical-align: top; padding-bottom: 10px; padding-top: 10px; font-size: 12px; color: #999999; text-align: center;">
#                                 <a href="https://tabaye.ir/" style="color: #999999; font-size: 12px; text-align: center; text-decoration: none;">طب سنتی برای همه © 1399 - تمامی حقوق محفوظ است</a>
#                             </td>
#                             </tr>
#                         </table>
#                         </div>
#                         <!-- END FOOTER -->

#                     <!-- END CENTERED WHITE CONTAINER -->
#                     </div>
#                     </td>
#                     <td style="font-family: sans-serif; font-size: 14px; vertical-align: top;">&nbsp;</td>
#                 </tr>
#                 </table>
#             </body>
#             </html>
#             """
#             html_result = html_result_1 + title_html + content_html + call_to_action_html + html_result_2

#             # Send email to consultant
#             # email = Email.objects.create(
#             #     user = user,
#             #     subject = "کد تایید",
#             #     html_message = html_result,
#             # )


#             return Response(new_data, status = HTTP_200_OK)

#         return Response(serializer.errors, status = HTTP_400_BAD_REQUEST)


# User Verification Check API View
# class UserVerificationCheckAPIView(APIView):
#     permission_classes = [AllowAny]
#     serializer_class = UserVerificationCheckSerializer

#     # POST
#     def post(self, request, *args, **kwargs):
#         data = request.data
#         serializer = UserVerificationCheckSerializer(data = data)
#         if serializer.is_valid(raise_exception = True):
#             data = serializer.data
#             # https://docs.djangoproject.com/en/dev/topics/auth/default/#changing-passwords
#             identity = data.get('identity')
#             code = data.get('code')
#             user = User.objects.filter(
#                 Q(username = identity) |
#                 Q(email = identity) |
#                 Q(phone = identity)
#             ).distinct().first()

#             # validate code and check its relation with user here...
#             user_code = user.codes.filter(code = code, used = False).distinct().first()
#             # user_code.used = True
#             # user_code.save()

#             return Response(data, status = HTTP_200_OK)

#         return Response(serializer.errors, status = HTTP_400_BAD_REQUEST)



