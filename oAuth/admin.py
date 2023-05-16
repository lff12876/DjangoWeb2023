from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext, gettext_lazy as _
from oAuth.models import User


# Register your models here.

class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('email',)}),
        (_('Permissions'), {'fields': ('is_staff', 'is_superuser', 'user_permissions', 'roles', 'times',
                                       'business_activate', 'fin_time')}),
        (_('Important dates'), {'fields': ('date_joined',)})
    )
    list_display = ('id', 'username', 'roles', 'email', 'times', 'business_activate', 'fin_time', 'last_login')
    list_display_links = ('id', 'username', 'roles', 'email', 'times', 'business_activate', 'fin_time', 'last_login')
    # list_filter = ('roles', )
    search_fields = ('username', 'email', 'id')
    '''10 items per page'''
    list_per_page = 50
    '''Max 200 when clicking show all'''
    list_max_show_all = 200  # default


class DataAdmin(admin.ModelAdmin):
    list_display = ('code', 'date', 'time', )
    search_fields = ('code', )
    '''10 items per page'''
    list_per_page = 50
    '''Max 200 when clicking show all'''
    list_max_show_all = 200  # default


admin.site.register(User, UserAdmin)
#admin.site.register(OauthTestdata, DataAdmin)


admin.site.site_title = "系统后台"
admin.site.site_header = "项目管理系统"
admin.site.index_title = "后台主页"
