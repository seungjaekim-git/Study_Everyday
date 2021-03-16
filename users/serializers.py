from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
    ValidationError,
    EmailField,
    CharField,
    )

from django.db.models import Q

from django.contrib.auth import get_user_model
User = get_user_model()

from users.utils import generate_access_token, generate_refresh_token
from django.contrib.auth import authenticate

from rest_framework_jwt.settings import api_settings

class UserDetailSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]

class UserCreateSerializer(ModelSerializer):
    email = EmailField(label="Email Address")
    email2 = EmailField(label="Confirm Email")
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password',
        ]

        extra_kwargs = {"password":
                        {"write_only": True}
                        }

    def validate(self, data):
        # email = data['email']
        # user_qs = User.objects.filter(email=email)
        # if user_qs.exists():
        #     raise ValidationError("This user has already registered.")

        return data


    def validate_email(self, value):
        data = self.get_initial()
        email1 = data.get("email2")
        email2 = value
        if email1 != email2:
            raise ValidationError("Emails must match!")

        user_qs = User.objects.filter(email=email2)
        if user_qs.exists():
            raise ValidationError("This email has already been registered.")

        return value 

    def create(self, validated_data):
        username         = validated_data['username']
        email            = validated_data['email']
        password         = validated_data['password']
        user_obj         = User(
                username = username,
                email    = email
            )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data



class UserLoginSerializer(ModelSerializer):
    
    token = CharField(allow_blank=True, read_only=True)
    username = CharField(required=False, allow_blank=True)
    email = EmailField(label="Email Address", required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'token',
        ]

        extra_kwargs = {"password":
                        {"write_only": True}
                        }

    def validate(self, data):
        user_obj = None
        email = data.get("email", None)
        password = data.get("password",None)

        if not email or not password:
            raise ValidationError("A username or email is required to login.")

        user = User.objects.filter(
                Q(email=email)
            ).distinct()
        user = user.exclude(email__isnull=True).exclude(email__iexact="")

        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError("This username/email is not valid.")

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect credentials please try again.")


        payload = api_settings.JWT_PAYLOAD_HANDLER(user_obj)
        jwt_token = api_settings.JWT_ENCODE_HANDLER(payload)
        data['token'] = jwt_token
        return data
            
