from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from oAuth.models import User, OauthTestdata
from rest_framework.response import Response

from oAuth.serializer import UserSerializer
from django.db.models import Q
from datetime import datetime
# Create your views here.

class UserInfoViewSet(viewsets.ViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        print('ok')
        # print(request)
        user_info = User.objects.filter(id=request.user.id).values()[0]
        role = request.user.roles
        if role == 0:
            user_info['roles'] = ['admin']
        else:
            user_info['roles'] = ['user']

        return Response(user_info)


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    #list_get creat_post

    def list(self, request, *args, **kwargs):
        user = request.user
        if user.roles == 1:
            self.queryset = self.queryset.filter(~Q(username='admin'))
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
#class LogoutViewSet(viewsets.ViewSet):
    #pass

@csrf_exempt
def user_logout(request):
    if request.method == 'GET':
        return HttpResponse(status=404)
    if request.method == 'POST':
        return HttpResponse(status=200)


def ad_home(request):
    return render(request, "home.html")


def usr_charts(request):
    return render(request, "multichart.html")


def usr_activity(request):
    return render(request, "activity.html")


def api_charts(request):
    code = request.GET.get('code')
    queryres = OauthTestdata.objects.all().values().filter(code=code)
    time_list = []
    for item in queryres:
        date = item['date']
        time = item['time']
        year = int(date/10000)
        month = int((date-year*10000)/100)
        day = date % 100
        hour = int(time/10000)
        minute = int((time-hour*10000)/100)
        sec = time % 100
        dt = datetime(year=year,month=month,day=day,hour=hour,minute=minute,second=sec)
        time_list.append(str(dt))
        #break
        #time_list.append(dt)

    context = {
        'queryset': queryres,
        'timelist': time_list,
    }
    return render(request, "usr_echarts.html", context)
    #return  HttpResponse(queryres)
