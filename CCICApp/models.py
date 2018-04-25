from django.db import models

# Create your models here.
class vvebo(models.Model):
    id = models.IntegerField(primary_key=True)
    keyword = models.TextField(max_length=1000, default="")
    user_id = models.TextField(max_length=1000, default="")
    user_name = models.TextField(max_length=1000, default="")
    time = models.CharField(max_length=1000, default="")
    comment = models.TextField(max_length=1000, default="")
    shoucang = models.IntegerField(default=0)
    zhuanfa = models.IntegerField(default=0)
    pinglun = models.IntegerField(default=0)
    dianzan = models.IntegerField(default=0)
    device = models.TextField(max_length=1000, default="")
    url = models.TextField(max_length=1000, default="")