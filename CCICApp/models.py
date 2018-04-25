from django.db import models

# 微博Model
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




# 知乎Model
class zhihu(models.Model):
    keyword = models.TextField(max_length=100, default="")
    question_id = models.CharField(max_length=20, default="")
    question_name = models.TextField(max_length=100, default="")
    answer_id = models.CharField(max_length=20, default="")
    comment = models.TextField(max_length=30000, default="")
    time = models.CharField(max_length=20, default="")
    voteup_count = models.IntegerField(default=0)
    user_name = models.CharField(max_length=20, default="")




#微信Model
class wechat(models.Model):
    id = models.IntegerField(primary_key=True)
    keyword = models.TextField(max_length=1000, default="")
    article_title = models.TextField(max_length=1000, default="")
    article_url = models.TextField(max_length=1000, default="")
    article_imgs = models.TextField(max_length=1000, default="")
    comment = models.TextField(max_length=1000, default="")
    time = models.TextField(max_length=1000, default="")
    gzh_profile_url =  models.TextField(max_length=1000, default="")
    gzh_headimage = models.TextField(max_length=1000, default="")
    user_name = models.TextField(max_length=1000, default="")
    gzh_isv = models.IntegerField(default=0)


