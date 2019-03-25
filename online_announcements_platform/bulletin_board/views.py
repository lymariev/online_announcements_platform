from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Announcement, Category
from .serializers import AnnouncementSerializer, CategorySerializer
from django_filters.rest_framework import DjangoFilterBackend


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class ReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return False


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.filter(is_hidden=False)
    serializer_class = AnnouncementSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'price')


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.exclude(parent=None)
    serializer_class = CategorySerializer
    permission_classes = (ReadOnly,)
