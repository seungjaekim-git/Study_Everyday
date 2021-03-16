from django.db.models import Q
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework     import status

from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)

from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
)

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)


from .serializers import (
    UserCreateSerializer,
    UserLoginSerializer,
    UserDetailSerializer
)
User = get_user_model()


class UserCreateAPIView(CreateAPIView):
    query_set = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

class UserLoginAPIView(APIView):

    serializer_class = UserLoginSerializer
    permission_class = [AllowAny]

    # def get(self, request, *args, **kwargs):
    #     return Response(status=HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            #response.set_cookie(key='refreshtoken',value=refresh_token,httponly=True)
            return Response(new_data, status=HTTP_200_OK) 
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class UserDetailAPIView(APIView):

    serializer_class = UserDetailSerializer
    permission_class = [IsAuthenticated]
    
    def get(self,request):
        payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
        print('payload 1 ' + str(payload))
        user = User.objects.get(id=payload['user_id'])
        
        return None

        
