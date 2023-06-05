import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.utils.translation import gettext_lazy as _


# Create your models here.
class User(AbstractUser):
    role_type = [
        [0, '管理员'],
        [1, '用户'],
    ]
    activate_type = [
        [0, '未激活'],
        [1, '已激活'],
    ]
    roles = models.IntegerField(verbose_name='角色', choices=role_type, default=1)
    last_login = models.DateTimeField(_('last login'), blank=True, null=True, auto_now=True)
    times = models.IntegerField(verbose_name='剩余次数', default=0)
    business_activate = models.IntegerField(verbose_name='业务激活', choices=activate_type, default=0)
    fin_time = models.DateTimeField(verbose_name='业务截至日期', blank=True, null=True)
    sign_ip = models.GenericIPAddressField(verbose_name='注册ip', blank=True, null=True)
    last_log_ip = models.GenericIPAddressField(verbose_name='上次登录ip', blank=True, null=True)
    max_key_num = models.IntegerField(verbose_name='最大密钥数量', default=2)
    code = models.UUIDField(verbose_name='识别码', db_column='code', default=uuid.uuid4, editable=False)
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        unique_together = ('email',)
        pass


class OauthSecretKey(models.Model):
    status_type = [
        [0, '激活'],
        [1, '警告'],
        [2, '锁定'],
        [3, '禁用'],
        [4, '警告并锁定'],
    ]
    key_type = [
        [0, '长期'],
        [1, '定期'],
    ]
    id = models.BigAutoField(primary_key=True)
    value = models.UUIDField(verbose_name='密钥', db_column='value', default=uuid.uuid4, editable=False)
    username = models.CharField(verbose_name='用户名', db_column='username', max_length=150)
    uid = models.ForeignKey(verbose_name='所属用户id', db_column='uid', to=User, to_field="id", on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(verbose_name='绑定ip', db_column='ip', blank=False, null=False)
    status = models.IntegerField(verbose_name='状态', db_column='status', choices=status_type, default=0)
    type = models.IntegerField(verbose_name='类型', db_column='type', choices=key_type, default=0)
    fin_time = models.DateTimeField(verbose_name='结束时间', db_column='fin_time', blank=True, null=True)
    last_query_time = models.DateTimeField(verbose_name='复盘数据上次请求时间', db_column='last_query_time', blank=True, null=True)
    last_query_time_today = models.DateTimeField(verbose_name='当日数据上次请求时间', db_column='last_query_time_today', blank=True, null=True)
    last_change_time = models.DateTimeField(verbose_name='上次变更时间', db_column='last_change_time', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'oauth_secretkey'


class OauthIp(models.Model):
    status_type = [
        [0, '激活'],
        [1, '黑名单'],
        [2, '白名单'],
    ]
    id = models.BigAutoField(primary_key=True)
    ip = models.GenericIPAddressField(db_column='ip', unique=True, blank=False, null=False)
    status = models.IntegerField(db_column='status', choices=status_type, default=0)
    max_key_num = models.IntegerField(db_column='max_key_num', default=10)

    class Meta:
        managed = True
        db_table = 'oauth_ip'


class OauthQueryLog(models.Model):
    log_type = [
        [0, '当日数据'],
        [1, '复盘数据'],
    ]
    id = models.BigAutoField(primary_key=True)
    uid = models.ForeignKey(verbose_name='所属用户id', db_column='uid', to=User, to_field="id",
                            on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(verbose_name='请求ip', db_column='ip', blank=False, null=False)
    type = models.IntegerField(verbose_name='请求类型', choices=log_type, db_column='type', blank=False, null=False)
    code = models.IntegerField(db_column='Code', blank=False, null=False)  # Field name made lowercase.
    date = models.IntegerField(db_column='Date', blank=False, null=False)  # Field name made lowercase.
    query_time = models.DateTimeField(db_column='query_time', blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'oauth_request_log'


class OauthStockData(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.IntegerField(db_column='Code', blank=True, null=True)  # Field name made lowercase.
    date = models.IntegerField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    time = models.IntegerField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    recloseprice = models.FloatField(db_column='ReClosePrice', blank=True, null=True)  # Field name made lowercase.
    matchprice = models.FloatField(db_column='MatchPrice', blank=True, null=True)  # Field name made lowercase.
    matchvol = models.IntegerField(db_column='MatchVol', blank=True, null=True)  # Field name made lowercase.
    askvol = models.IntegerField(db_column='AskVol', blank=True, null=True)  # Field name made lowercase.
    matchincrease = models.FloatField(db_column='MatchIncrease', blank=True, null=True)  # Field name made lowercase.
    matchmoney = models.FloatField(db_column='Matchmoney', blank=True, null=True)  # Field name made lowercase.
    hardenprice = models.FloatField(db_column='HardenPrice', blank=True, null=True)  # Field name made lowercase.
    limitdownprice = models.FloatField(db_column='LimitDownPrice', blank=True, null=True)  # Field name made lowercase.
    up = models.FloatField(blank=True, null=True)
    down = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'oauth_stockdata'
        index_together = ["code", "date"]

class OauthTodayData(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.IntegerField(db_column='Code', blank=True, null=True)  # Field name made lowercase.
    date = models.IntegerField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    time = models.IntegerField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    recloseprice = models.FloatField(db_column='ReClosePrice', blank=True, null=True)  # Field name made lowercase.
    matchprice = models.FloatField(db_column='MatchPrice', blank=True, null=True)  # Field name made lowercase.
    matchvol = models.IntegerField(db_column='MatchVol', blank=True, null=True)  # Field name made lowercase.
    askvol = models.IntegerField(db_column='AskVol', blank=True, null=True)  # Field name made lowercase.
    matchincrease = models.FloatField(db_column='MatchIncrease', blank=True, null=True)  # Field name made lowercase.
    matchmoney = models.FloatField(db_column='Matchmoney', blank=True, null=True)  # Field name made lowercase.
    hardenprice = models.FloatField(db_column='HardenPrice', blank=True, null=True)  # Field name made lowercase.
    limitdownprice = models.FloatField(db_column='LimitDownPrice', blank=True, null=True)  # Field name made lowercase.
    up = models.FloatField(blank=True, null=True)
    down = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'oauth_todaydata'
        index_together = ["code", "date"]


