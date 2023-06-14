from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class MsgHistory(models.Model):
    id=models.AutoField(primary_key=True,verbose_name='id')
    foruser=models.ForeignKey('auth.User',on_delete=models.DO_NOTHING,verbose_name="发送人")
    crtime=models.DateTimeField(auto_now=True,verbose_name="发送时间")
    msgs=models.TextField(verbose_name="消息内容",null=True, blank=True)
    class Meta:
        verbose_name='消息列表'
        verbose_name_plural=verbose_name
        ordering = ['-crtime']
    def __str__(self):
        return str(self.id)