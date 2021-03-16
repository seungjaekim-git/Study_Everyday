from rest_framework import viewsets
from .serializers import BoardSerializer, CommentSerializer
from .models import Board, Comment, Appendix
from rest_framework import permissions

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user

class BoardViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    permission_classes = (IsOwnerOrReadOnly,)

    authentication_classes = (JSONWebTokenAuthentication,)

class CommentViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    permission_classes = (IsOwnerOrReadOnly,)

    authentication_classes = (JSONWebTokenAuthentication)
