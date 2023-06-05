from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext, gettext_lazy as _
from oAuth.models import User,OauthSecretKey


# Register your models here.

class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('email',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'roles', 'times',
                                       'business_activate', 'fin_time')}),
        (_('Important dates'), {'fields': ('date_joined',)})
    )
    list_display = ('id', 'username', 'roles', 'email', 'is_active', 'times', 'business_activate', 'fin_time', 'last_login')
    list_display_links = ('id', 'username', 'roles', 'email', 'times', 'business_activate', 'fin_time', 'last_login')
    # list_filter = ('roles', )
    search_fields = ('username', 'email', 'id')
    '''10 items per page'''
    list_per_page = 20
    '''Max 200 when clicking show all'''
    list_max_show_all = 200  # default


class SecretkeyAdmin(admin.ModelAdmin):
    list_display = ['id', 'value', 'username', 'uid', 'ip', 'status', 'last_query_time', 'last_change_time']
    list_editable = ['status']
    list_filter = ['username', 'uid']
    search_fields = ['username', 'uid', 'ip', 'status']
    list_per_page = 20
    list_max_show_all = 200  # default
    pass


admin.site.register(User, UserAdmin)
admin.site.register(OauthSecretKey, SecretkeyAdmin)
#admin.site.register(OauthTestdata, DataAdmin)


admin.site.site_title = "系统后台"
admin.site.site_header = "项目管理系统"
admin.site.index_title = "后台主页"
