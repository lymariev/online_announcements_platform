from django.urls import include, path
from django.views.generic.base import RedirectView
from . import views


urlpatterns = [
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('account/', include('allauth.urls')),
    path('accounts/profile/', RedirectView.as_view(url='/', permanent=True), name='profile-redirect'),
    path('rest-auth/facebook/', views.FacebookLogin.as_view(), name='fb_login'),
    path('rest-auth/twitter/', views.TwitterLogin.as_view(), name='twitter_login'),
    path('rest-auth/facebook/connect/', views.FacebookConnect.as_view(), name='fb_connect'),
    path('rest-auth/twitter/connect/', views.TwitterConnect.as_view(), name='twitter_connect')
]