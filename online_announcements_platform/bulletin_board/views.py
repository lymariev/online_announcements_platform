from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Announcement, Category
from .serializers import AnnouncementSerializer, CategorySerializer
from django_filters.rest_framework import DjangoFilterBackend


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.filter(is_hidden=False)
    serializer_class = AnnouncementSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'price')

    @action(methods=['post'], detail=True, permission_classes=(permissions.IsAuthenticated,),
            url_path='add-to-favorites', url_name='add_to_favorites')
    def add_to_favorites(self, request, pk=None):
        announcement = self.get_queryset().get(pk=pk)
        announcement.in_favorites.add(request.user)
        return Response(status=status.HTTP_200_OK)

    @action(methods=['delete'], detail=True, permission_classes=(permissions.IsAuthenticated,),
            url_path='delete-from-favorites', url_name='delete_from_favorites')
    def delete_from_favorites(self, request, pk=None):
        announcement = self.get_queryset().get(pk=pk)
        announcement.in_favorites.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False, permission_classes=(permissions.IsAuthenticated,),
            url_path='favorites', url_name='favorites')
    def get_favorites_list(self, request):
        queryset = self.get_queryset().filter(in_favorites=request.user)
        serializer = AnnouncementSerializer(queryset, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.exclude(parent=None)
    serializer_class = CategorySerializer
