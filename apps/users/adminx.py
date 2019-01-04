import xadmin
from users.models import EmailVerifyRecord, Banner

@xadmin.sites.register(EmailVerifyRecord)
class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email','send_type', 'send_time']
    search_fields = ['code', 'email','send_type']
    list_filter = ['code', 'email','send_type', 'send_time']


@xadmin.sites.register(Banner)
class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']
# xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)