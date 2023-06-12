from django.urls import path, include
from oAuth.models import User, OauthSecretKey, OauthIp
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
#drf的序列化类，建立后才能通过drf实现的接口进行传参等操作

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password','roles', 'email', 'times', 'business_activate', 'fin_time', 'last_login',
                  'sign_ip']


class SecretkeySerializer(serializers.ModelSerializer):
    class Meta:
        model = OauthSecretKey
        fields = ['id', 'value', 'username', 'uid', 'ip', 'status', 'type', 'fin_time', 'last_query_time',
                  'last_change_time']


class IpSerializer(serializers.ModelSerializer):
    class Meta:
        model = OauthIp
        fields = ['id', 'ip', 'status', 'max_key_num', ]