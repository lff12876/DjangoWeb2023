from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

from djangoTest import settings
from oAuth.models import User, OauthStockData, OauthTodayData, OauthSecretKey, OauthIp, OauthQueryLog
from rest_framework.response import Response
from django.core.mail import send_mail

from oAuth.serializer import UserSerializer, SecretkeySerializer, IpSerializer
from django.db.models import Q
import datetime
import pytz
from django.utils import timezone


def convert_to_localtime(utctime):
    fmt = '%Y-%m-%d %H:%M:%S'
    utc = utctime.replace(tzinfo=pytz.UTC)
    localtz = utc.astimezone(timezone.get_current_timezone())
    return localtz.strftime(fmt)


def convert_to_local_datetime(utctime):
    fmt = '%Y-%m-%d %H:%M:%S.%f'
    utc = utctime.replace(tzinfo=pytz.UTC)
    localtz = utc.astimezone(timezone.get_current_timezone())
    str = localtz.strftime(fmt)
    date = datetime.datetime.strptime(str, fmt)
    return date


# Create your views here.


class UserInfoViewSet(viewsets.ViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        user_info = User.objects.filter(id=request.user.id).values()[0]
        # user = User.objects.filter(id=request.user.id).values()[0]
        utctime = user_info['last_login']
        fin_utc_time = user_info['fin_time']
        cntime = convert_to_localtime(utctime)
        fin_time = None
        dt = datetime.datetime.now()
        if fin_utc_time is not None:
            fin_time = convert_to_localtime(fin_utc_time)
            ft = convert_to_local_datetime(fin_utc_time)
            if ft < dt:
                user = User.objects.get(id=request.user.id)
                user.business_activate = 0
                user_info['business_activate'] = 0
                user.save()
        user_info['password'] = ['']
        user_info['last_login'] = cntime
        user_info['fin_time'] = fin_time
        bus_status = user_info['business_activate']
        role = request.user.roles
        if bus_status == 0:
            user_info['business_activate'] = ['未激活']
        else:
            user_info['business_activate'] = ['已激活']
        if role == 0:
            user_info['roles'] = ['管理员']
        else:
            user_info['roles'] = ['普通用户']
        return Response(user_info)


# ViewSets define the view behavior.
class UserCreateViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post', 'get']
    permission_classes = []

    # list_get creat_post update_put/patch destory_delete

    def retrieve(self, request, *args, **kwargs):
        instance = User.objects.get(code=kwargs['pk'])
        instance.is_active = True
        instance.save()
        data = {
            'status': 'success',
        }
        return render(request, 'active_success.html')

    def create(self, request, *args, **kwargs):
        # get real ip address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        # get serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_info = self.perform_create(serializer)
        # set sign in ip
        user_info.sign_ip = ip
        user_info.is_active = False
        if request.data['password'] == request.data['repassword']:
            user_info.set_password(request.data['password'])
            user_info.save()
            code = user_info.code
            url = request.build_absolute_uri("/api/user/active/" + str(code) + "/")
            username = user_info.username
            subject = '账户激活-' + username
            from_email = settings.EMAIL_HOST_USER
            to_email = user_info.email
            meg_html = '<a href="' + url + '">点击激活</a>'
            send_mail(subject, meg_html, from_email, [to_email])
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            data = {
                'error': '密码校验错误,请重试'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        return serializer.save()


class UserChangeViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['patch']
    def update(self, request, *args, **kwargs):
        user_id = request.user.id
        instance = self.get_object()
        if user_id == instance.id:
            psw = request.data['password']
            instance.set_password(psw)
            instance.save()
            data = {
                'success': '修改成功'
            }
            return Response(data, status=status.HTTP_202_ACCEPTED)
        else:
            data = {
                'error': '校验错误'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class SecretKeyViewSet(viewsets.ModelViewSet):
    queryset = OauthSecretKey.objects.all()
    serializer_class = SecretkeySerializer
    http_method_names = ['get', 'post', 'put', 'patch']

    def list(self, request, *args, **kwargs):
        queryset = OauthSecretKey.objects.filter(uid=request.user.id)
        instance = queryset.values()[0]
        last_change_time = instance['last_change_time']
        last_query_time = instance['last_query_time']
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = serializer.data
            if last_change_time is not None:
                lct = convert_to_localtime(last_change_time)
                data[0]['last_change_time'] = lct
            if last_query_time is not None:
                lqt = convert_to_localtime(last_query_time)
                data[0]['last_query_time'] = lqt
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # get real ip address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        query_keys = OauthSecretKey.objects.filter(uid=request.user.id)
        if len(query_keys) > 0:
            data = {
                'error': '您已拥有密钥，请勿重复申请！'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = request.data
            data['ip'] = ip
            data['uid'] = request.user.id
            data['username'] = request.user.username
            data['last_change_time'] = datetime.datetime.now()
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        data = {}
        instance = self.get_object()
        # get real ip address
        query_type = request.query_params['type']
        query_key = request.query_params['key']
        if query_type == "ip":
            if instance.uid == request.user:
                last_change_time = instance.last_change_time
                dt = datetime.datetime.now()
                l_changetime = convert_to_local_datetime(last_change_time)
                if (dt-l_changetime).seconds < 1800:
                    data['error'] = '修改间隔不能小于30分钟'
                    return Response(data, status.HTTP_400_BAD_REQUEST)
                else:
                    instance.last_change_time = dt
                    instance.save()
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[-1].strip()
                else:
                    ip = request.META.get('REMOTE_ADDR')
                if instance.ip != ip:
                    instance.ip = ip
                    instance.save()
                return Response(data, status.HTTP_202_ACCEPTED)
            else:
                data['error'] = '校验错误'
        else:
            if instance.uid == request.user:
                if instance.status == 0 or instance.status == 1:
                    return Response(data, status.HTTP_202_ACCEPTED)
                elif instance.status == 2:
                    instance.status = 0
                    instance.save()
                    return Response(data, status.HTTP_202_ACCEPTED)
                elif instance.status == 4:
                    instance.status = 1
                    instance.save()
                    return Response(data, status.HTTP_202_ACCEPTED)
                elif instance.status == 3:
                    data['error'] = '密钥已被禁用'
        return Response(data, status.HTTP_400_BAD_REQUEST)


class LinkViewSet(viewsets.ModelViewSet):
    queryset = OauthSecretKey.objects.all()
    serializer_class = SecretkeySerializer
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        data = {}
        queryset = OauthSecretKey.objects.filter(uid=request.user.id)
        if len(queryset) > 0:
            key_instance = queryset.values()[0]
            data['key'] = key_instance['value']
            data['base_url'] = request.build_absolute_uri("/query")
            return Response(data)
        else:
            return Response(data, status.HTTP_404_NOT_FOUND)


class IpViewSet(viewsets.ModelViewSet):
    queryset = OauthIp.objects.all()
    serializer_class = IpSerializer

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

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


def user_logout(request):
    if request.method == 'GET':
        return HttpResponse(status=200)
    if request.method == 'POST':
        return HttpResponse(status=404)


def ad_home(request):
    return render(request, "home.html")


def usr_activity(request):
    return render(request, "activity.html")


def api_charts(request):
    code = request.GET.get('code')
    date = request.GET.get('date')
    secretkey = request.GET.get('secretkey')
    if secretkey is None:
        return HttpResponse(status.HTTP_403_FORBIDDEN)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    keys = OauthSecretKey.objects.filter(value=secretkey)
    err_data = {}
    if len(keys) > 0:
        key_instance = keys.values()[0]
        uid = key_instance['uid_id']
        user = User.objects.get(id=uid)
        if user.business_activate == 0:
            err_data['error'] = '业务未激活'
            return render(request, "key_error.html", err_data)
        user_fin_time = user.fin_time
        cur_time = datetime.datetime.now()
        user_ft = convert_to_local_datetime(user_fin_time)
        if cur_time > user_ft:
            user.business_activate = 0
            user.save()
            err_data['error'] = '业务已过期'
            return render(request, "key_error.html", err_data)
        if ip == key_instance['ip']:
            if key_instance['status'] == 0 or key_instance['status'] == 1:
                if_frequent = False
                if key_instance['last_query_time'] is None:
                    key = OauthSecretKey.objects.get(id=key_instance['id'])
                    key.last_query_time = datetime.datetime.now()
                    key.save()
                else:
                    last_query_time = key_instance['last_query_time']
                    lq_time = convert_to_local_datetime(last_query_time)
                    cur_time = datetime.datetime.now()
                    days = (cur_time-lq_time).days
                    seconds = (cur_time-lq_time).seconds
                    if days == 0 and seconds == 0 and (cur_time-lq_time).microseconds < 100000:
                        key = OauthSecretKey.objects.get(id=key_instance['id'])
                        if key_instance['status'] == 0:
                            key.status = 1
                            key.last_query_time = cur_time
                            key.save()
                            err_data['error'] = '警告，请求过于频繁，再次频繁请求时密钥将被禁用'
                            if_frequent = True
                        else:
                            key.status = 3
                            key.last_query_time = cur_time
                            key.save()
                            err_data['error'] = '多次频繁请求，密钥已被禁用'
                            if_frequent = True
                if not if_frequent:
                    key = OauthSecretKey.objects.get(id=key_instance['id'])
                    key.last_query_time = cur_time
                    key.save()
                    if date is None:
                        dt = datetime.datetime.now()
                        date_value = dt.year * 10000 + dt.month * 100 + dt.day
                        date_str = str(dt.year) + '年' + str(dt.month) + '月' + str(dt.day) + '日'
                    else:
                        dt = datetime.datetime.strptime(date, '%Y-%m-%d')
                        date_value = dt.year * 10000 + dt.month * 100 + dt.day
                        date_str = str(dt.year) + '年' + str(dt.month) + '月' + str(dt.day) + '日'
                    log = OauthQueryLog(uid=user, type=1, code=code, date=date_value, query_time=datetime.datetime.now(), ip=ip)
                    log.save()
                    queryres = OauthStockData.objects.all().values().filter(code=code, date=date_value)
                    yesterday = dt + datetime.timedelta(days=-1)
                    tomorrow = dt + datetime.timedelta(days=+1)
                    yesterday_str = str(yesterday.year) + '-' + str(yesterday.month) + '-' + str(yesterday.day)
                    tomorrow_str = str(tomorrow.year) + '-' + str(tomorrow.month) + '-' + str(tomorrow.day)
                    time_list = []
                    for item in queryres:
                        date = item['date']
                        time = item['time']
                        year = int(date / 10000)
                        month = int((date - year * 10000) / 100)
                        day = date % 100
                        hour = int(time / 10000)
                        minute = int((time - hour * 10000) / 100)
                        sec = time % 100
                        dt = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=sec)
                        time_list.append(str(dt))
                    url = request.build_absolute_uri("/query/charts/?secretkey="+str(key_instance['value']))
                    context = {
                        'queryset': queryres,
                        'timelist': time_list,
                        'code': code,
                        'date': date,
                        'date_str': date_str,
                        'yesterday_str': yesterday_str,
                        'tomorrow_str': tomorrow_str,
                        'jmp_str': url,
                    }
                    return render(request, "usr_echarts.html", context)
            else:
                err_data['error'] = '密钥状态异常'
                return render(request, "key_error.html", err_data)
        elif key_instance['status'] == 0 or key_instance['status'] == 2:
            key = OauthSecretKey.objects.get(id=key_instance['id'])
            key.status = 2
            key.save()
            err_data['error'] = 'ip异常，密钥已被锁定'
        elif key_instance['status'] == 1 or key_instance['status'] == 4:
            key = OauthSecretKey.objects.get(id=key_instance['id'])
            key.status = 4
            key.save()
            err_data['error'] = 'ip异常，密钥已被锁定'
        else:
            err_data['error'] = '密钥状态异常'
    else:
        err_data['error'] = '密钥不存在'
    return render(request, "key_error.html", err_data)

def api_charts_today(request):
    code = request.GET.get('code')
    secretkey = request.GET.get('secretkey')
    if secretkey is None:
        return HttpResponse(status.HTTP_403_FORBIDDEN)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    keys = OauthSecretKey.objects.filter(value=secretkey)
    err_data = {}
    if len(keys) > 0:
        key_instance = keys.values()[0]
        uid = key_instance['uid_id']
        user = User.objects.get(id=uid)
        if user.times <= 0:
            err_data['error'] = '剩余查询次数不足'
            return render(request, "key_error.html", err_data)
        if ip == key_instance['ip']:
            if key_instance['status'] == 0 or key_instance['status'] == 1:
                if_frequent = False
                if not if_frequent:
                    key = OauthSecretKey.objects.get(id=key_instance['id'])
                    key.save()
                    dt = datetime.datetime.now()
                    date_value = dt.year * 10000 + dt.month * 100 + dt.day
                    log = OauthQueryLog(uid=user, type=0, code=code, date=date_value, query_time=datetime.datetime.now(), ip=ip)
                    log.save()
                    date_str = str(dt.year) + '年' + str(dt.month) + '月' + str(dt.day) + '日'
                    queryres = OauthTodayData.objects.all().values().filter(code=code, date=20230505)
                    if len(queryres) != 0:
                        user.times -= 1
                        user.save()
                    time_list = []
                    for item in queryres:
                        date = item['date']
                        time = item['time']
                        year = int(date / 10000)
                        month = int((date - year * 10000) / 100)
                        day = date % 100
                        hour = int(time / 10000)
                        minute = int((time - hour * 10000) / 100)
                        sec = time % 100
                        dt = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=sec)
                        time_list.append(str(dt))
                    context = {
                        'queryset': queryres,
                        'timelist': time_list,
                        'code': code,
                        'date_str': date_str,
                    }
                    return render(request, "usr_echart_today.html", context)
            else:
                err_data['error'] = '密钥状态异常'
                return render(request, "key_error.html", err_data)
        elif key_instance['status'] == 0 or key_instance['status'] == 2:
            key = OauthSecretKey.objects.get(id=key_instance['id'])
            key.status = 2
            key.save()
            err_data['error'] = 'ip异常，密钥已被锁定'
        elif key_instance['status'] == 1 or key_instance['status'] == 4:
            key = OauthSecretKey.objects.get(id=key_instance['id'])
            key.status = 4
            key.save()
            err_data['error'] = 'ip异常，密钥已被锁定'
        else:
            err_data['error'] = '密钥状态异常'
    else:
        err_data['error'] = '密钥不存在'
    return render(request, "key_error.html", err_data)

