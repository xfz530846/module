from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

from mlh.utils.models import BaseModel
from users import constants


class User(AbstractUser):
    """用户模型类"""
    #由于超级管理员的手机号为空，同时注册的时候序列化器进行过手机号检测，顾这里默认值为空
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号',null=True,default=None)
    #管理员默认昵称为admin,用户注册时候会走其他流程昵称改为用户注册账号
    nickname = models.CharField(max_length=32, verbose_name='用户昵称',default='admin')
    avatar_url = models.CharField(max_length=128, verbose_name='用户头像',default= constants.HOST + 'default_pic/u=2922170376,2371336021&fm=26&gp=0.jpg')

    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

class UserArchives(models.Model):
    """用户个人中心"""

    Gender_CHOICES = (
        (1, "男"),
        (2, "女"),
    )
    user = models.OneToOneField(User, on_delete=models.PROTECT,verbose_name='用户')
    gender = models.SmallIntegerField(verbose_name='性别',choices=Gender_CHOICES,default=None,null=True)
    birthdate = models.DateField(verbose_name='出生日期',default=None,null=True)
    real_mobile = models.CharField(max_length=11,verbose_name='个人档案手机号',default=None,null=True)
    experience = models.TextField(verbose_name='工作经历',default=None,null=True)
    fort = models.CharField(verbose_name='擅长技能',max_length=64,default=None,null=True)
    address = models.CharField(verbose_name='通讯地址',max_length=64,default=None,null=True)
    realname = models.CharField(max_length=32,verbose_name='真实姓名',default=None,null=True)
    city = models.CharField(max_length=32, verbose_name='所在城市', default=None,null=True)
    edu = models.CharField(max_length=32, verbose_name='毕业院校', default=None,null=True)
    company = models.CharField(max_length=32, verbose_name='所在公司', default=None,null=True)
    intro = models.CharField(max_length=64, verbose_name='个人简介', default=None,null=True)
    website = models.CharField(max_length=128, verbose_name='个人网站', default=None,null=True)
    email = models.CharField(max_length=128, verbose_name='个人邮箱', default=None,null=True)
    realphoto = models.ImageField(max_length=64,verbose_name='真实照片', default=None,null=True)

    class Meta:
        db_table = 'user_archives'
        verbose_name = '用户档案'
        verbose_name_plural = verbose_name


class FansFollowed(BaseModel):
    """用户关注模型"""

    fans = models.ForeignKey(User, on_delete=models.PROTECT, related_name='fans', verbose_name='用户粉丝')
    followeds = models.ForeignKey(User, on_delete=models.PROTECT, related_name='followeds', verbose_name='用户关注')

    class Meta:
        db_table = 'users_fansfollowed'
        verbose_name = '用户关注和粉丝'
        verbose_name_plural = verbose_name


class MyActive(BaseModel):
    """我的动态"""
    # user = models.ForeignKey(User,verbose_name='用户',on_delete=models.CASCADE)
    pass
