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
#从应用oAuth中引入ViewSet
from oAuth.views import UserInfoViewSet, UserCreateViewSet, UserChangeViewSet, SecretKeyViewSet, LinkViewSet, IpViewSet
from django.views.generic import TemplateView
#路由配置
#此处为drf实现的API路由
router_V1 = routers.DefaultRouter()
router_V1.register('info', UserInfoViewSet)
router_V1.register('user/create', UserCreateViewSet)
router_V1.register('user/active', UserCreateViewSet)
router_V1.register('user_change_pwd', UserChangeViewSet)
router_V1.register('secretkey', SecretKeyViewSet)
router_V1.register('link', LinkViewSet)
router_V1.register('ip', IpViewSet)

urlpatterns = [
    path('api/', include(router_V1.urls)),#DRF实现的API路由都被划分为‘api/’的子路由
    path('admin/', admin.site.urls),#管理员后台访问路由
    path('', TemplateView.as_view(template_name="index.html")),#打包后的vue项目主页
    path('activity/', views.usr_activity),#广告页预留
    path('query/charts/', views.api_charts),#复盘数据接口
    path('query/today/', views.api_charts_today),#当日数据接口
    path('api/login/', TokenObtainPairView.as_view(), name='token-obtain-pair'),#simple_jwt优雅的实现校验登录，如要更改校验逻辑，要建立继承ModelBackend类重写authenticate函数
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),#刷新token
    path('api/logout/', views.user_logout),#登出功能
]
