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

class Zhihu(models.Model):
    keyword = models.TextField(max_length=100, default="")
    question_id = models.CharField(max_length=20, default="")
    question_name = models.TextField(max_length=100, default="")
    answer_id = models.CharField(max_length=20, default="")
    comment = models.TextField(max_length=30000, default="")
    time = models.CharField(max_length=20, default="")
    voteup_count = models.IntegerField(default=0)
    user_name = models.CharField(max_length=20, default="")