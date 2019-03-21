from django.urls import include, path
from django.contrib import admin
from rest_framework_swagger.views import get_swagger_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', get_swagger_view(title='API Docs'), name='api_docs'),
    path('', include(('reg_auth.urls', 'reg_auth'), namespace='reg_auth')),
]
