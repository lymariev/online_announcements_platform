from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('announcements', views.AnnouncementViewSet)
router.register('categories', views.CategoryViewSet)

urlpatterns = router.urls
