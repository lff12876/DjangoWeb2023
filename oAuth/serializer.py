from django.urls import path, include
from oAuth.models import User
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'roles', 'email', 'times', 'business_activate', 'fin_time', 'last_login']