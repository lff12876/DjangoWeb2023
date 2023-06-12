from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

from djangoTest import settings
from oAuth.models import User, OauthStockData, OauthTodayData, OauthSecretKey, OauthIp, OauthQueryLog
from oAuth.models import stockdata20204, stockdata20214, stockdata20211, stockdata20212, stockdata20213, stockdata20221\
    , stockdata20222
from oAuth.models import stockdata20223, stockdata20224, stockdata20231, stockdata20232
from django.db import connection
from rest_framework.response import Response
from django.core.mail import send_mail

from oAuth.serializer import UserSerializer, SecretkeySerializer, IpSerializer
from django.db.models import Q
import datetime
import pytz
from django.utils import timezone
#主要业务逻辑在此处实现

# 节假日处理，方便实现翻页逻辑
holidays = ['2023-04-29', '2023-04-30', '2023-05-01', '2023-05-02', '2023-05-03', '2023-06-22', '2023-06-23',
            '2023-06-24', '2023-09-29', '2023-09-30', '2023-10-01', '2023-10-02', '2023-10-03', '2023-10-04',
            '2023-10-05', '2023-10-06']
min_date = datetime.datetime(year=2023, month=4, day=24)

#此处为预留的数据分表后根据日期判断表的情况
def date_switch(dt):
    if dt.year == 2020:
        return stockdata20204
    elif dt.year == 2021:
        if dt.month < 4:
            return stockdata20211
        elif dt.month < 7:
            return stockdata20212
        elif dt.month < 10:
            return stockdata20213
        else:
            return stockdata20214
    elif dt.year == 2022:
        if dt.month < 4:
            return stockdata20221
        elif dt.month < 7:
            return stockdata20222
        elif dt.month < 10:
            return stockdata20223
        else:
            return stockdata20224
    else:
        if dt.month < 4:
            return stockdata20231
        else:
            return OauthStockData

#utc时间转化为 '%Y-%m-%d %H:%M:%S' 格式的当前时区时间字符串
def convert_to_localtime(utctime):
    fmt = '%Y-%m-%d %H:%M:%S'
    utc = utctime.replace(tzinfo=pytz.UTC)
    localtz = utc.astimezone(timezone.get_current_timezone())
    return localtz.strftime(fmt)

#utc时间转化为 '%Y-%m-%d %H:%M:%S.%f' 格式的当前时区时间，带.%f处理microsecond
def convert_to_local_datetime(utctime):
    fmt = '%Y-%m-%d %H:%M:%S.%f'
    utc = utctime.replace(tzinfo=pytz.UTC)
    localtz = utc.astimezone(timezone.get_current_timezone())
    str = localtz.strftime(fmt)
    date = datetime.datetime.strptime(str, fmt)
    return date


# Create your views here.
#drf 实现RESTFUL标准的接口
#继承ViewSet重写的函数名与请求种类的对应关系
#list 对应get请求
#creat 对应post请求
#update 对应put请求和patch请求
#destory 对应delete请求

#pycharm开发时可通过按住ctrl+点击的方式跳转到继承的ViesSet类源码，便于学习


#drf实现的获取用户信息的ViewSet
class UserInfoViewSet(viewsets.ViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    http_method_names = ['get']#仅允许get请求

    def list(self, request, *args, **kwargs):
        user_info = User.objects.filter(id=request.user.id).values()[0]
        # user = User.objects.filter(id=request.user.id).values()[0]
        utctime = user_info['last_login']
        fin_utc_time = user_info['fin_time']
        cntime = convert_to_localtime(utctime)#时区转换
        fin_time = None
        dt = datetime.datetime.now()
        if fin_utc_time is not None:#处理空值
            fin_time = convert_to_localtime(fin_utc_time)
            ft = convert_to_local_datetime(fin_utc_time)
            if ft < dt:#判断业务是否过期
                user = User.objects.get(id=request.user.id)
                user.business_activate = 0
                user_info['business_activate'] = 0
                user.save()
        user_info['password'] = ['']#隐藏密码信息
        user_info['last_login'] = cntime
        user_info['fin_time'] = fin_time
        bus_status = user_info['business_activate']
        role = request.user.roles
        if bus_status == 0:#设置状态文本
            user_info['business_activate'] = ['未激活']
        else:
            user_info['business_activate'] = ['已激活']
        if role == 0:#设置类型文本
            user_info['roles'] = ['管理员']
        else:
            user_info['roles'] = ['普通用户']
        return Response(user_info)


# ViewSets define the view behavior.
#注册用户业务实现
class UserCreateViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post', 'get']#允许get post
    permission_classes = []#注册接口，需要移除权限验证

    # list_get creat_post update_put/patch destory_delete

    #retrieve对应对单条数据的get，请求链接中应有唯一标识该条数据的值
    def retrieve(self, request, *args, **kwargs):
        instance = User.objects.get(code=kwargs['pk'])#用户激活，根据code获取用户实例
        instance.is_active = True#设置激活
        instance.save()#保存
        data = {
            'status': 'success',
        }
        return render(request, 'active_success.html')

    #用户注册
    def create(self, request, *args, **kwargs):
        # get real ip address
        #获取真实ip地址，此处注意Nginx配置的参数
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
        user_info.is_active = False#默认设置非激活
        if request.data['password'] == request.data['repassword']:#校验注册两次输入的密码是否相同
            user_info.set_password(request.data['password'])#用django原生的set_password设置密码，数据库中存储的是加密后的密码
            code = user_info.code
            url = request.build_absolute_uri("/api/user/active/" + str(code) + "/")#生成激活链接
            username = user_info.username
            #构造邮件
            subject = '账户激活-' + username#标题
            from_email = settings.EMAIL_HOST_USER#邮件来源
            to_email = user_info.email#邮件目的
            meg_html = '欢迎注册测试版系统，请访问您的专有链接以激活账户：' + url#激活链接
            try:
                send_mail(subject, meg_html, from_email, [to_email])
                user_info.save()#发送成功后保存
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            except Exception as e:
                user_info.delete()#异常退出则删掉刚刚创建的用户
                data = {
                    'error': e
                }
                return Response(data, status.HTTP_400_BAD_REQUEST)
        else:
            data = {
                'error': '密码校验错误,请重试'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        return serializer.save()

#用户修改密码接口
class UserChangeViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['patch']#仅允许patch

    def update(self, request, *args, **kwargs):#此处的request中的user是根据解析token获得的，此处已完成权限验证
        user_id = request.user.id
        instance = self.get_object()
        if user_id == instance.id:#校验链接中的id与token对应的id是否相同
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

#密钥接口
class SecretKeyViewSet(viewsets.ModelViewSet):
    queryset = OauthSecretKey.objects.all()
    serializer_class = SecretkeySerializer
    http_method_names = ['get', 'post', 'put', 'patch']

    #查询密钥
    def list(self, request, *args, **kwargs):
        queryset = OauthSecretKey.objects.filter(uid=request.user.id)#根据token解析出的用户id做筛选
        if len(queryset) > 0:#如果密钥存在
            instance = queryset.values()[0]
            last_change_time = instance['last_change_time']
            last_query_time = instance['last_query_time']
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                data = serializer.data
                if last_change_time is not None:
                    lct = convert_to_localtime(last_change_time)#转换时区
                    data[0]['last_change_time'] = lct
                if last_query_time is not None:
                    lqt = convert_to_localtime(last_query_time)#转换时区
                    data[0]['last_query_time'] = lqt
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:#空值处理，默认
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

    #创建密钥
    def create(self, request, *args, **kwargs):
        # get real ip address
        #获取反向代理前的真实ip地址
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        query_keys = OauthSecretKey.objects.filter(uid=request.user.id)
        if len(query_keys) > 0:#已有密钥无法重复申请，若后续要允许一个用户拥有多个密钥，需修改此处
            data = {
                'error': '您已拥有密钥，请勿重复申请！'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = request.data
            data['ip'] = ip
            data['uid'] = request.user.id
            data['username'] = request.user.username
            data['last_change_time'] = datetime.datetime.now()#记录上次变更时间
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    #更新密钥状态
    def update(self, request, *args, **kwargs):
        data = {}
        instance = self.get_object()
        # get real ip address
        query_type = request.query_params['type']
        query_key = request.query_params['key']
        if query_type == "ip":#更改绑定ip
            if instance.uid == request.user:#校验请求的用户与token解析的用户是否一致
                last_change_time = instance.last_change_time#获取密钥上次变更时间
                dt = datetime.datetime.now()
                l_changetime = convert_to_local_datetime(last_change_time)#时区转换
                if (dt - l_changetime).seconds < 1800:#时间间隔判断
                    data['error'] = '修改间隔不能小于30分钟'
                    return Response(data, status.HTTP_400_BAD_REQUEST)
                else:
                    instance.last_change_time = dt#更新上次变更时间
                    instance.save()#保存
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[-1].strip()
                else:
                    ip = request.META.get('REMOTE_ADDR')
                if instance.ip != ip:#如果ip变更了则修改，否则不修改
                    instance.ip = ip
                    instance.save()#保存
                return Response(data, status.HTTP_202_ACCEPTED)
            else:
                data['error'] = '校验错误'
        else:#变更密钥状态，主要用于解除锁定
            if instance.uid == request.user:#校验用户
                if instance.status == 0 or instance.status == 1:#正常 或 警告 状态，直接返回
                    return Response(data, status.HTTP_202_ACCEPTED)
                elif instance.status == 2:#锁定状态转正常
                    instance.status = 0
                    instance.save()
                    return Response(data, status.HTTP_202_ACCEPTED)
                elif instance.status == 4:#警告并锁定状态转警告状态
                    instance.status = 1
                    instance.save()
                    return Response(data, status.HTTP_202_ACCEPTED)
                elif instance.status == 3:#禁用状态无法解锁
                    data['error'] = '密钥已被禁用'
        return Response(data, status.HTTP_400_BAD_REQUEST)#返回错误信息


#生成链接接口
class LinkViewSet(viewsets.ModelViewSet):
    queryset = OauthSecretKey.objects.all()
    serializer_class = SecretkeySerializer
    http_method_names = ['get']#仅允许get

    def list(self, request, *args, **kwargs):
        data = {}
        queryset = OauthSecretKey.objects.filter(uid=request.user.id)
        if len(queryset) > 0:
            key_instance = queryset.values()[0]
            data['key'] = key_instance['value']#密钥值
            data['base_url'] = request.build_absolute_uri("/query")#基本链接，会根据访问链接自动生成
            return Response(data)#返回key 和 base_url 由前端自己拼接呈现链接
        else:#无密钥时的处理
            data['error'] = '您还没有密钥，请申请密钥后重试'
            return Response(data, status.HTTP_404_NOT_FOUND)


#预留的ip接口，此处代码与mixins.py内的相同
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

#以下为django原生方法实现的接口，未使用drf

#登出，返回状态码，前端移除token
def user_logout(request):
    if request.method == 'GET':
        return HttpResponse(status=200)
    if request.method == 'POST':
        return HttpResponse(status=404)

#预留的广告主页
def ad_home(request):
    return render(request, "home.html")

#预留的活动页
def usr_activity(request):
    return render(request, "activity.html")

#用户请求复盘数据接口
def api_charts(request):
    code = request.GET.get('code')#获取请求中的code
    date = request.GET.get('date')#获取date，可能为空
    secretkey = request.GET.get('secretkey')#获取密钥
    if secretkey is None:#参数中无密钥的情况
        err_data = {
            'error': '校验错误'
        }
        return render(request, "key_error.html", err_data)
    #获取真实ip
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    #查询密钥是否存在
    keys = OauthSecretKey.objects.filter(value=secretkey)
    err_data = {}
    #如果密钥存在
    if len(keys) > 0:
        key_instance = keys.values()[0]
        uid = key_instance['uid_id']
        user = User.objects.get(id=uid)#获取用户信息
        if user.business_activate == 0:#业务激活状态判断，未激活直接返回
            err_data['error'] = '业务未激活'
            return render(request, "key_error.html", err_data)
        user_fin_time = user.fin_time#获取业务结束时间
        cur_time = datetime.datetime.now()
        user_ft = convert_to_local_datetime(user_fin_time)
        if cur_time > user_ft:#校验业务是否到期
            user.business_activate = 0#设置状态为未激活
            user.save()
            err_data['error'] = '业务已过期'#过期返回
            return render(request, "key_error.html", err_data)
        if ip == key_instance['ip']:#判断请求ip是否与密钥绑定ip相同
            if key_instance['status'] == 0 or key_instance['status'] == 1:#相同则查看密钥状态，是否为正常或警告
                if_frequent = False#设置标志记录是否请求过于频繁
                if key_instance['last_query_time'] is None:#如果过去没请求过数据，更新最近请求时间
                    key = OauthSecretKey.objects.get(id=key_instance['id'])
                    key.last_query_time = datetime.datetime.now()
                    key.save()
                else:#计算时间差，判断是否访问过于频繁
                    last_query_time = key_instance['last_query_time']
                    lq_time = convert_to_local_datetime(last_query_time)#时区转换
                    cur_time = datetime.datetime.now()#当前时间
                    days = (cur_time - lq_time).days
                    seconds = (cur_time - lq_time).seconds
                    #此处的坑，python datetime  中microseconds只记录时间中不足一秒的时间有多少微秒，要结合days和seconds判断是否高频
                    if days == 0 and seconds == 0 and (cur_time - lq_time).microseconds < 100000:#如果请求间隔小于0.1秒
                        key = OauthSecretKey.objects.get(id=key_instance['id'])
                        if key_instance['status'] == 0:#若原本密钥状态正常
                            key.status = 1#设为警告状态
                            key.last_query_time = cur_time#更新上次查询时间
                            key.save()
                            err_data['error'] = '警告，请求过于频繁，再次频繁请求时密钥将被禁用'
                            if_frequent = True#设置频繁标记
                        else:#其他情况直接禁用密钥
                            key.status = 3
                            key.last_query_time = cur_time#更新上次查询时间
                            key.save()
                            err_data['error'] = '多次频繁请求，密钥已被禁用'
                            if_frequent = True
                if not if_frequent:#如果非高频访问
                    key = OauthSecretKey.objects.get(id=key_instance['id'])
                    key.last_query_time = cur_time#更新上次请求时间
                    key.save()
                    max_date = datetime.datetime.now()
                    if max_date.weekday() == 5:#如果当前时间为周六
                        max_date = max_date + datetime.timedelta(days=-1)
                    if max_date.weekday() == 6:#周日
                        max_date = max_date + datetime.timedelta(days=-2)
                    if date is None:#如果无date参数，自动设为最近的历史数据
                        dt = max_date
                        lastday = dt + datetime.timedelta(days=-1)#上一天
                        while lastday.weekday() == 5 or lastday.weekday() == 6 or lastday.strftime(  # 周末和节假日跳过
                                '%Y-%m-%d') in holidays:
                            lastday = lastday + datetime.timedelta(days=-1)
                            if lastday.date() <= min_date.date():
                                lastday = min_date
                        dt = lastday
                        date = dt.strftime('%Y-%m-%d')
                        date_value = dt.year * 10000 + dt.month * 100 + dt.day#转换为数据库中的int型日期
                        date_str = str(dt.year) + '年' + str(dt.month) + '月' + str(dt.day) + '日'
                    else:
                        dt = datetime.datetime.strptime(date, '%Y-%m-%d')#有date，转化为datetime类型
                        if dt>max_date:
                            dt = max_date
                        date = dt.strftime('%Y-%m-%d')
                        date_value = dt.year * 10000 + dt.month * 100 + dt.day#转化为数据库中的int型日期
                        date_str = str(dt.year) + '年' + str(dt.month) + '月' + str(dt.day) + '日'
                    log = OauthQueryLog(uid=user, type=1, code=code, date=date_value,
                                        query_time=datetime.datetime.now(), ip=ip)#用户请求写入日志
                    log.save()
                    #stockdb = date_switch(dt)#分表时使用
                    #queryres = stockdb.objects.all().values().filter(code=code, date=date_value)#获取数据 分表的情况
                    queryres = OauthStockData.objects.all().values().filter(code=code, date=date_value)#获取数据
                    yesterday = dt + datetime.timedelta(days=-1)#上一天，用于翻页
                    tomorrow = dt + datetime.timedelta(days=+1)#下一天，用于翻页
                    while yesterday.weekday() == 5 or yesterday.weekday() == 6 or yesterday.strftime(#周末和节假日跳过
                            '%Y-%m-%d') in holidays:
                        yesterday = yesterday + datetime.timedelta(days=-1)
                        if yesterday.date() <= min_date.date():
                            yesterday = min_date
                    while tomorrow.weekday() == 5 or tomorrow.weekday() == 6 or tomorrow.strftime(
                            '%Y-%m-%d') in holidays:
                        tomorrow = tomorrow + datetime.timedelta(days=+1)
                        if tomorrow.date() >= max_date.date():
                            tomorrow = max_date
                    yesterday_str = str(yesterday.year) + '-' + str(yesterday.month) + '-' + str(yesterday.day)
                    tomorrow_str = str(tomorrow.year) + '-' + str(tomorrow.month) + '-' + str(tomorrow.day)
                    time_list = []#时间单独发送，用于前端echarts的时间类型x轴
                    index = 0
                    flag = False
                    index920 = 0#记录9点20之后的首个数据在列表中的位置
                    for item in queryres:
                        date = item['date']
                        time = item['time']
                        year = int(date / 10000)
                        month = int((date - year * 10000) / 100)
                        day = date % 100
                        hour = int(time / 10000)
                        minute = int((time - hour * 10000) / 100)
                        sec = time % 100
                        if hour == 9 and minute >= 20 and flag is False:
                            index920 = index
                            flag = True
                        dt = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=sec)
                        time_list.append(str(dt))#把int型时间转化为时间字符串
                        index = index + 1
                    url = request.build_absolute_uri("/query/charts/?secretkey=" + str(key_instance['value']))#url，用于翻页跳转构造链接
                    context = {
                        'queryset': queryres,#数据
                        'timelist': time_list,#时间
                        'code': code,
                        'date': date,
                        'date_str': date_str,
                        'yesterday_str': yesterday_str,
                        'tomorrow_str': tomorrow_str,
                        'jmp_str': url,
                        'index_920': index920,
                    }
                    return render(request, "usr_echarts.html", context)
            else:#密钥为不可用状态
                err_data['error'] = '密钥状态异常'
                return render(request, "key_error.html", err_data)
        elif key_instance['status'] == 0 or key_instance['status'] == 2:#ip校验未通过
            key = OauthSecretKey.objects.get(id=key_instance['id'])#密钥状态设为锁定
            key.status = 2
            key.save()
            err_data['error'] = 'ip异常，密钥已被锁定'
        elif key_instance['status'] == 1 or key_instance['status'] == 4:
            key = OauthSecretKey.objects.get(id=key_instance['id'])#密钥状态设为警告并锁定
            key.status = 4
            key.save()
            err_data['error'] = 'ip异常，密钥已被锁定'
        else:#密钥已被禁用
            err_data['error'] = '密钥状态异常'
    else:#密钥不存在
        err_data['error'] = '密钥不存在'
    return render(request, "key_error.html", err_data)


#当日数据查询接口，与复盘数据接口类似
def api_charts_today(request):
    code = request.GET.get('code')
    secretkey = request.GET.get('secretkey')
    #不用加日期参数
    if secretkey is None:#密钥参数是否为空
        err_data = {
            'error': '校验错误'
        }
        return render(request, "key_error.html", err_data)
    #获取真实ip
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    keys = OauthSecretKey.objects.filter(value=secretkey)
    err_data = {}
    if len(keys) > 0:#密钥存在
        key_instance = keys.values()[0]
        uid = key_instance['uid_id']
        user = User.objects.get(id=uid)#获取用户信息
        if user.times <= 0:#判断剩余查询次数
            err_data['error'] = '剩余查询次数不足'
            return render(request, "key_error.html", err_data)
        if ip == key_instance['ip']:
            if key_instance['status'] == 0 or key_instance['status'] == 1:
                if_frequent = False#预留，可加频率控制
                if not if_frequent:
                    key = OauthSecretKey.objects.get(id=key_instance['id'])
                    key.save()
                    max_date = datetime.datetime.now()
                    while max_date.weekday() == 5 or max_date.weekday() == 6 or max_date.strftime(#周末和节假日跳过
                            '%Y-%m-%d') in holidays:
                        max_date = max_date + datetime.timedelta(days=-1)
                        if max_date.date() <= min_date.date():
                            max_date = min_date
                    dt = max_date
                    date_value = dt.year * 10000 + dt.month * 100 + dt.day
                    log = OauthQueryLog(uid=user, type=0, code=code, date=date_value,
                                        query_time=datetime.datetime.now(), ip=ip)
                    log.save()#写入日志
                    date_str = str(dt.year) + '年' + str(dt.month) + '月' + str(dt.day) + '日'
                    queryres = OauthTodayData.objects.all().values().filter(code=code, date=20230505)#测试数据为20230505的数据，正式使用时修改 改为date_value则查询当日数据，若表只存一天的数据，可只根据code查询
                    if len(queryres) != 0:#未查询到数据不减扣次数
                        user.times -= 1
                        user.save()
                    time_list = []
                    index = 0
                    flag = False
                    index920 = 0
                    for item in queryres:
                        date = item['date']
                        time = item['time']
                        year = int(date / 10000)
                        month = int((date - year * 10000) / 100)
                        day = date % 100
                        hour = int(time / 10000)
                        minute = int((time - hour * 10000) / 100)
                        sec = time % 100
                        if hour == 9 and minute >= 20 and flag is False:
                            index920 = index
                            flag = True
                        dt = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=sec)
                        time_list.append(str(dt))
                        index = index + 1
                    context = {
                        'queryset': queryres,
                        'timelist': time_list,
                        'code': code,
                        'date_str': date_str,
                        'index_920': index920,
                    }
                    return render(request, "usr_echart_today.html", context)
            else:#异常状态处理同复盘数据处理
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
