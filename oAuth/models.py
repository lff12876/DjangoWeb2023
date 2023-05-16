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
        [0, '已激活'],
        [1, '未激活'],
    ]
    roles = models.IntegerField(verbose_name='角色', choices=role_type, default=1)
    last_login = models.DateTimeField(_('last login'), blank=True, null=True, auto_now=True)
    times = models.IntegerField(verbose_name='剩余次数', default=0)
    business_activate = models.IntegerField(verbose_name='业务激活', choices=activate_type, default=0)
    fin_time = models.DateTimeField(verbose_name='业务截至日期', blank=True, null=True)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        pass


class OauthTestdata(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.IntegerField(db_column='Code', blank=True, null=True)  # Field name made lowercase.
    date = models.IntegerField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    time = models.IntegerField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    recloseprice = models.FloatField(db_column='ReClosePrice', blank=True, null=True)  # Field name made lowercase.
    matchprice = models.FloatField(db_column='MatchPrice', blank=True, null=True)  # Field name made lowercase.
    matchvol = models.IntegerField(db_column='MatchVol', blank=True, null=True)  # Field name made lowercase.
    askvol = models.IntegerField(db_column='AskVol', blank=True, null=True)  # Field name made lowercase.
    matchincrease = models.IntegerField(db_column='MatchIncrease', blank=True, null=True)  # Field name made lowercase.
    matchmoney = models.FloatField(db_column='Matchmoney', blank=True, null=True)  # Field name made lowercase.
    hardenprice = models.FloatField(db_column='HardenPrice', blank=True, null=True)  # Field name made lowercase.
    limitdownprice = models.FloatField(db_column='LimitDownPrice', blank=True, null=True)  # Field name made lowercase.
    up = models.FloatField(blank=True, null=True)
    down = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'oauth_testdata'
        index_together = ["code", "date"]

