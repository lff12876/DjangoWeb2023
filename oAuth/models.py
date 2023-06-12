import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.utils.translation import gettext_lazy as _


# Create your models here.
# 在此处定义models，使得开发者可以跳过sql语言，直接操作models来操作数据库

#继承AbstractUser的用户类
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
        unique_together = ('email',)#设置邮箱号唯一
        pass


class OauthSecretKey(models.Model):
    status_type = [#密钥状态
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
    last_query_time = models.DateTimeField(verbose_name='复盘数据上次请求时间', db_column='last_query_time', blank=True, null=True)#用来控制访问频率
    last_query_time_today = models.DateTimeField(verbose_name='当日数据上次请求时间', db_column='last_query_time_today', blank=True, null=True)
    last_change_time = models.DateTimeField(verbose_name='上次变更时间', db_column='last_change_time', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'oauth_secretkey'#表名

#预留的ip类，可用于设计同ip注册人数和使用密钥人数限制功能
class OauthIp(models.Model):
    status_type = [
        [0, '激活'],
        [1, '黑名单'],
        [2, '白名单'],
    ]
    id = models.BigAutoField(primary_key=True)
    ip = models.GenericIPAddressField(db_column='ip', unique=True, blank=False, null=False)
    status = models.IntegerField(db_column='status', choices=status_type, default=0)#状态
    max_key_num = models.IntegerField(db_column='max_key_num', default=10)#最大密钥数

    class Meta:
        managed = True
        db_table = 'oauth_ip'#表名

#用户查询日志
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

#预留的日期类，可用于限制用户请求，可用于记录数据上传状态方便管理
class OauthDate(models.Model):
    store_type = [
        [0, '未存储'],
        [1, '已存储'],
    ]
    date = models.DateField(primary_key=True, verbose_name='日期', db_column='Date')
    status = models.IntegerField(verbose_name='状态', blank=False, null=False, choices=store_type, default=0)

    class Meta:
        managed = True
        db_table = 'oauth_date'

#重要的大表，存放复盘数据
#若试用期数据量不超过一个季度，使用一个表即可
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
        db_table = 'oauth_stockdata'#表名
        index_together = ["code", "date"]#建立索引，针对code和date的‘与’查询定向优化性能

#当日数据，运营过程中需定时清空，运维人员可根据具体情况决定是否每日一清，如果仅存放一天的数据，可简化查询罗逻辑，仅查询code
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
        index_together = ["code", "date"]#定向优化，与复盘数据类似

class stockdata20204(models.Model):#此类及以下为分表预留
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
        db_table = 'oauth_stockdata20204'
        index_together = ["code", "date"]  # 建立索引，针对code和date的‘与’查询定向优化性能

class stockdata20211(models.Model):
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
        db_table = 'oauth_stockdata20211'
        index_together = ["code", "date"]  # 建立索引，针对code和date的‘与’查询定向优化性能

class stockdata20212(models.Model):
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
        db_table = 'oauth_stockdata20212'
        index_together = ["code", "date"]  # 建立索引，针对code和date的‘与’查询定向优化性能


class stockdata20213(models.Model):
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
        db_table = 'oauth_stockdata20213'

class stockdata20214(models.Model):
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
        db_table = 'oauth_stockdata20214'

class stockdata20221(models.Model):
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
        db_table = 'oauth_stockdata20221'


class stockdata20222(models.Model):
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
        db_table = 'oauth_stockdata20222'

class stockdata20223(models.Model):
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
        db_table = 'oauth_stockdata20223'

class stockdata20224(models.Model):
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
        db_table = 'oauth_stockdata20224'

class stockdata20231(models.Model):
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
        db_table = 'oauth_stockdata20231'

class stockdata20232(models.Model):
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
        db_table = 'oauth_stockdata20232'
