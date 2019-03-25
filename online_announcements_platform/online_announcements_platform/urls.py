from django.urls import include, path
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_swagger.views import get_swagger_view

urlpatterns = [
    path('', include('reg_auth.urls')),
    path('', get_swagger_view(title='API Docs'), name='api_docs'),
    path('', include(('bulletin_board.urls', 'bulletin_board'), namespace='bulletin_board')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
