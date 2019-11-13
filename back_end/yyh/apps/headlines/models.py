from django.db import models

from mlh.utils.models import BaseModel
from ckeditor_uploader.fields import RichTextUploadingField

from questions.models import AskLables
from users.models import User


class Categories(BaseModel):
    """头条分类模型"""

    CATEGORY_SEQUENCE_ENUM = {
        "FIRST": 1,
        "SECOND": 2,
        "THIRD": 3,
        "FOUTH": 4,
        "FIFTH": 5,
        "SIXTH": 6,
    }

    CATEGORY_SEQUENCE_CHOICES = (
        (1, "FIRST"),
        (2, "SECOND"),
        (3, "THIRD"),
        (4, "FOUTH"),
        (5, "FIFTH"),
        (6, "SIXTH"),

    )

    name = models.CharField(max_length=10, unique=True, verbose_name="分类名称")
    sequence = models.IntegerField(choices=CATEGORY_SEQUENCE_CHOICES, verbose_name="序号")  # 控制页面显示顺序

    class Meta:
        db_table = "headlines_categories"
        verbose_name = "头条分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Headlines(BaseModel):
    """头条模型"""

    NEWS_STATUS_ENUM = {
        "UNAPPROVED": -1,
        "CHECKING": 0,
        "APPROVED": 1
    }

    NEWS_STATUS_CHOICES = (
        (-1, "UNAPPROVED"), # 未通过审核
        (0, "CHECKING"),  # 审核中
        (1, "APPROVED"),  # 通过审核
    )

    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="作者")
    category = models.ForeignKey(Categories, on_delete=models.PROTECT, verbose_name="头条分类")
    title = models.CharField(max_length=64, verbose_name="头条标题")
    content = RichTextUploadingField(verbose_name="头条内容")
    image = models.CharField(max_length=128, null=True, default=None, verbose_name="头条图片链接")
    comment_counts = models.IntegerField(default=0, verbose_name="头条评论数")
    click_counts = models.IntegerField(default=0, verbose_name="浏览量")
    status = models.IntegerField(choices=NEWS_STATUS_CHOICES, default=NEWS_STATUS_ENUM["CHECKING"], verbose_name="头条状态")
    reason = models.CharField(max_length=40, null=True, default=None, verbose_name="未通过审核原因")


    class Meta:
        db_table = "headlines"
        verbose_name = "头条"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Comments(models.Model):
    """头条评论模型"""
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="用户")
    headlines = models.ForeignKey(Headlines, on_delete=models.CASCADE, verbose_name="头条")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, default=None, verbose_name="父评论")
    content = models.CharField(max_length=128, verbose_name="评论内容")
    create_time = models.DateTimeField(auto_now=True, verbose_name="创建时间")
    child_counts = models.IntegerField(default=0, verbose_name="子评论数量")  # 冗余字段, 方便查找

    class Meta:
        db_table = "headlines_comments"
        verbose_name = "评论"
        verbose_name_plural = verbose_name


class HeadlinesCollections(BaseModel):
    """头条收藏模型"""

    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="用户")
    headlines = models.ForeignKey(Headlines, on_delete=models.CASCADE, verbose_name="头条")

    class Meta:
        db_table = "user_headlines_collections"
        verbose_name = "头条收藏"
        verbose_name_plural = verbose_name


class Carousel(BaseModel):
    """轮播图模型"""

    CAROUSEL_SEQUENCE_ENUM = {
        "FIRST": 1,
        "SECOND": 2,
        "THIRD": 3,
        "FOUTH": 4,
        "FIFTH": 5
    }

    CAROUSEL_SEQUENCE_CHOICES = (
        (1, "FIRST"),
        (2, "SECOND"),
        (3, "THIRD"),
        (4, "FOUTH"),
        (5, "FIFTH")
    )

    image = models.CharField(max_length=128, verbose_name="图片链接")
    target = models.CharField(max_length=128, verbose_name="跳转链接")
    sequence = models.IntegerField(choices=CAROUSEL_SEQUENCE_CHOICES, verbose_name="序号") 

    class Meta:
        db_table = "carousels"
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name


class HeadlinesLabel(BaseModel):
    """头条标签模型"""

    label = models.ForeignKey(AskLables, on_delete=models.CASCADE, verbose_name='头条标签')
    headline = models.ForeignKey(Headlines, on_delete=models.CASCADE, verbose_name='头条标签')




class BroswingHistory(BaseModel):
    """浏览记录"""
    user = models.ForeignKey(User,verbose_name='用户',on_delete=models.CASCADE,)
    headlines = models.ForeignKey(Headlines,verbose_name='浏览记录',on_delete=models.CASCADE,)
    class Meta:
        db_table = 'broswing_history'
        verbose_name = '浏览记录'
        verbose_name_plural = verbose_name
