import xadmin
from users.models import EmailVerifyRecord, Banner


from xadmin import views

# xadmin的主题功能配置
@xadmin.sites.register(views.BaseAdminView)
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


#xadmin的全局样式配置
@xadmin.sites.register(views.CommAdminView)
class GlobalSettings(object):
    site_title = "xadmin后台管理系统"
    site_footer = "Arrowarcher"
    menu_style = "accordion"


@xadmin.sites.register(EmailVerifyRecord)
class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


@xadmin.sites.register(Banner)
class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']
# xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
