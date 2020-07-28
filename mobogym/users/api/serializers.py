from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime
from django.utils import timezone


User = get_user_model()


# User Create Serializer
class UserCreateSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(required = False)
    # password = CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True, label='Confirm Password')
    
    
    # Meta
    class Meta:
        model = User
        fields = [
            # 'username',
            'first_name',
            'last_name',
            # 'phone',
            'email',
            'age',
            'gender',
            'password',
            'password2',
        ]
        extra_kwargs = {"password":
                            {
                                "write_only": True,
                                'style':{'input_type': 'password'},
                                # "error_messages": {"required": "Give yourself a username"}
                            },
                        # 'password2':
                        #     {'write_only': True}
                        }

    # Validate the whole data here or in seprate functions
    # def validate(self, data):
    #     username = data['username']
    #     username_qs = User.objects.filter(username=username)
    #     if username_qs.exists():
    #         raise ValidationError('This Username has already been taken.')
    #     email = data['email']
    #     email_qs = User.objects.filter(email=email)
    #     if email_qs.exists():
    #         raise ValidationError("This Email address has already been registered.")
    #     return data

    # Validate email
    def validate_email(self, value):
        email = value
        if email or email != "":
            qs = User.objects.filter(email = email)
            if qs.exists():
                raise ValidationError(_("Email has already been registered!"))
        return value

    # Validate phone
    def validate_phone(self, value):
        phone = value
        if phone or phone != "":
            qs = User.objects.filter(phone = phone)
            if qs.exists():
                raise ValidationError(_("Phone has already been registered!"))
        return value

    # Validate password
    def validate_password(self, value):
        data = self.get_initial()
        password2 = data.get("password2")
        password = value
        if password != password2:
            raise ValidationError(_("Password does not match!"))
        if len(password) < 8:
            raise ValidationError(_("The password must be at least 8 characters long!"))
        first_isalpha = password[0].isalpha()
        if all(c.isalpha() == first_isalpha for c in password):
            raise ValidationError(_("The password must have at least one letter and at least one digit or character."))       
        try:
            # validate the password and catch the exception
            errors = {}
            validate_password(password=password, user=User)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            # errors['password'] = list(e.messages)
            errors = list(e.messages)

        if errors:
            raise ValidationError(errors)

        return value

    # Create
    def create(self, validated_data):
        # username = validated_data['username']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        # phone = validated_data['phone']
        email = validated_data['email']
        age = validated_data['age']
        gender = validated_data['gender']
        password = validated_data['password']
        user_obj = User(
                username = email,
                first_name = first_name,
                last_name = last_name,
                # phone = phone,
                email = email,
                age = age,
                gender = gender,
                # is_active = False,
                is_active = True,
                # is_staff = True,
            )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


# User List Serializer
class UserListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    
    
    # Meta
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'url'
        ]
        read_only_fields = ['username',]

    # get user
    def get_user(self, obj):
        return (obj.user.get_full_name())

    # get url
    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request = request)


# User Detail Serializer
class UserDetailSerializer(serializers.ModelSerializer):
    
    
    # Meta
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'phone',
            'birth_date',
            'first_name',
            'last_name'
        ]
        read_only_fields = ['username', 'id']


# User Login Serializer
class UserLoginSerializer(serializers.ModelSerializer):
    # username = CharField()
    # email = EmailField(label='Email Address')
    ID = serializers.CharField(label = 'User', help_text = 'Username Or Email Address Or Phone Number')
    token = serializers.CharField(allow_blank=True, read_only=True)
    
    
    # Meta
    class Meta:
        model = User
        fields = [
            # 'username',
            # 'email',
            'ID',
            'password',
            'token'
        ]
        extra_kwargs = {"password":
                            {
                                "write_only": True,
                                'style':{'input_type': 'password'},
                            },
                        # 'username':
                        #     {'help_text': '', 'required': False, 'allow_blank': True},

                            }

    def validate(self, data):
        user_obj = None
        identity = data.get('ID')
        password = data.get('password')
        user = User.objects.filter(
            Q(username = identity) |
            Q(email = identity) |
            Q(phone = identity)
        ).distinct()

        if user.exists() and user.count() == 1 :
            user_obj = user.first()
        else :
            raise ValidationError('This User is not valid.')

        if user_obj :
            if not user_obj.check_password(password):
                # raise ValidationError('Incorrect credentials.')
                raise ValidationError('This User is not valid.')

        data['token'] = 'SOME RANDOM TOKEN'
        return data


# Group
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name", )


# User Verification Serializer => Send code
class UserVerificationSerializer(serializers.ModelSerializer):
    identity = serializers.CharField(label = 'User', help_text = 'Username Or Email Address Or Phone Number')


    # Meta
    class Meta:
        model = User
        fields = [
            'identity',
        ]

    # Validate
    def validate(self, data):
        user_obj = None
        identity = data.get('identity')
        user = User.objects.filter(
            Q(username = identity) |
            Q(email = identity) |
            Q(phone = identity)
        ).distinct()

        if user.exists() and user.count() == 1 :
            user_obj = user.first()
        else :
            raise ValidationError({"error": _('This User is not valid.')})

        return data


# User Verify Serializer => Check and validate code
class UserVerificationCheckSerializer(serializers.ModelSerializer):
    identity = serializers.CharField(label = 'User', help_text = 'Username Or Email Address Or Phone Number')
    code = serializers.CharField(label = 'Code')
    class Meta:
        model = User
        fields = [
            'identity',
            'code',
        ]

    # Validate
    def validate(self, data):
        identity = data.get('identity')
        code = data.get('code')
        user = User.objects.filter(
            Q(username = identity) |
            Q(email = identity) |
            Q(phone = identity)
        ).distinct()

        if user.exists() and user.count() == 1 :
            user = user.first()
        else :
            raise ValidationError({"error": _('This User is not valid.')})
        
        # validate code and check its relation with user here...
        user_code = user.codes.filter(code = code, used = False).distinct().first()
        if user_code:
            now = timezone.now()
            if (user_code.expiration <= now):
                raise ValidationError({"error": _('Token has expired!')})
        else :
            raise ValidationError({"error": _('Token is not valid!')})

        return data


# User Reset Password Serializer 
class UserResetPasswordSerializer(serializers.ModelSerializer):
    identity = serializers.CharField(label = 'User', help_text = 'Username Or Email Address Or Phone Number')
    code = serializers.CharField(label = 'Code')
    new_password = serializers.CharField(label = 'New Password')


    # Meta
    class Meta:
        model = User
        fields = [
            'identity',
            'code',
            'new_password',
        ]

    # Validate
    def validate(self, data):
        user_obj = None
        identity = data.get('identity')
        code = data.get('code')
        new_password = data.get('new_password')
        user = User.objects.filter(
            Q(username = identity) |
            Q(email = identity) |
            Q(phone = identity)
        ).distinct()

        if user.exists() and user.count() == 1 :
            user = user.first()
        else :
            raise ValidationError({"error": _('This User is not valid.')})
        
        # validate code and check its relation with user here...
        user_code = user.codes.filter(code = code, used = False).distinct().first()
        if user_code:
            now = timezone.now()
            if (user_code.expiration <= now):
                raise ValidationError({"error": _('Token has expired!')})
        else :
            raise ValidationError({"error": _('Token is not valid!')})

        return data

# User check email Serializer
class UserCheckEmailSerializer(serializers.ModelSerializer):
    
    
    # Meta
    class Meta:
        model = User
        fields = [
            'email',
        ]





