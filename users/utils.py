import datetime
import jwt
from chatu import settings
from rest_framework.permissions import BasePermission, SAFE_METHODS


def generate_access_token(user):

    access_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=5),
        'iat': datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload,
                              settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
    return access_token


def generate_refresh_token(user):
    refresh_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }
    refresh_token = jwt.encode(
        refresh_token_payload, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')

    return refresh_token

class UserInfoPermission(BasePermission):
     message = 'You must be the owner of this object.'
     def has_object_permission(self, request, view, obj):
        # member = Membership.objects.get(user=request.user)
        # member.is_active()
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user

