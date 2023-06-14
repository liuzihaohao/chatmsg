from django.contrib import admin
from .models import *

# Register your models here.

class MsgHistoryAdmin(admin.ModelAdmin):
	list_display = ['id','msgs','foruser','crtime']
	list_display_links = ['id','msgs']
	search_fields = ['msgs','foruser']
	list_filter=['crtime']
admin.site.register(MsgHistory,MsgHistoryAdmin)

admin.site.site_title="ChatMsg"
admin.site.site_header="ChatMsg"