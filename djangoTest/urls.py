"""djangoTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import routers

from oAuth import views
from oAuth.views import UserInfoViewSet, UserCreateViewSet, UserChangeViewSet, SecretKeyViewSet, LinkViewSet, IpViewSet
from django.views.generic import TemplateView

router_V1 = routers.DefaultRouter()
router_V1.register('info', UserInfoViewSet)
router_V1.register('user/create', UserCreateViewSet)
router_V1.register('user/active', UserCreateViewSet)
router_V1.register('user_change_pwd', UserChangeViewSet)
router_V1.register('secretkey', SecretKeyViewSet)
router_V1.register('link', LinkViewSet)
router_V1.register('ip', IpViewSet)

urlpatterns = [
    path('api/', include(router_V1.urls)),
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="index.html")),
    path('activity/', views.usr_activity),
    path('query/charts/', views.api_charts),
    path('query/today/', views.api_charts_today),
    path('api/login/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', views.user_logout),
]
