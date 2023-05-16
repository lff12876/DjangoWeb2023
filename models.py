# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('OauthUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class OauthTestdata(models.Model):

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


class OauthUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    roles = models.IntegerField()
    last_login = models.DateTimeField(blank=True, null=True)
    times = models.IntegerField()
    business_activate = models.IntegerField()
    fin_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth_user'


class OauthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(OauthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'oauth_user_groups'
        unique_together = (('user', 'group'),)


class OauthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(OauthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'oauth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class TableName(models.Model):
    code = models.IntegerField(blank=True, null=True)
    time = models.IntegerField(blank=True, null=True)
    bst1 = models.FloatField(db_column='BST1', blank=True, null=True)  # Field name made lowercase.
    bst2 = models.FloatField(db_column='BST2', blank=True, null=True)  # Field name made lowercase.
    bst3 = models.FloatField(db_column='BST3', blank=True, null=True)  # Field name made lowercase.
    bst4 = models.FloatField(db_column='BST4', blank=True, null=True)  # Field name made lowercase.
    bst5 = models.FloatField(db_column='BST5', blank=True, null=True)  # Field name made lowercase.
    bst6 = models.FloatField(db_column='BST6', blank=True, null=True)  # Field name made lowercase.
    bst7 = models.FloatField(db_column='BST7', blank=True, null=True)  # Field name made lowercase.
    amo1 = models.FloatField(db_column='AMO1', blank=True, null=True)  # Field name made lowercase.
    amo2 = models.FloatField(db_column='AMO2', blank=True, null=True)  # Field name made lowercase.
    amo3 = models.FloatField(db_column='AMO3', blank=True, null=True)  # Field name made lowercase.
    amo4 = models.FloatField(db_column='AMO4', blank=True, null=True)  # Field name made lowercase.
    amo5 = models.FloatField(db_column='AMO5', blank=True, null=True)  # Field name made lowercase.
    amo6 = models.FloatField(db_column='AMO6', blank=True, null=True)  # Field name made lowercase.
    amo7 = models.FloatField(db_column='AMO7', blank=True, null=True)  # Field name made lowercase.
    b1 = models.FloatField(db_column='B1', blank=True, null=True)  # Field name made lowercase.
    b2 = models.FloatField(db_column='B2', blank=True, null=True)  # Field name made lowercase.
    b3 = models.FloatField(db_column='B3', blank=True, null=True)  # Field name made lowercase.
    b4 = models.FloatField(db_column='B4', blank=True, null=True)  # Field name made lowercase.
    b5 = models.FloatField(db_column='B5', blank=True, null=True)  # Field name made lowercase.
    b6 = models.FloatField(db_column='B6', blank=True, null=True)  # Field name made lowercase.
    b7 = models.FloatField(db_column='B7', blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(max_length=20, blank=True, null=True)
    date = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'table_name'
