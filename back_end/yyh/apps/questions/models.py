from django.db import models

# Create your models here.
from mlh.utils.models import BaseModel
from users.models import User


class AskLables(BaseModel):
    name=models.CharField(max_length=20,verbose_name="名称")
    focus_count=models.IntegerField(default=0,verbose_name="关注数")
    sequence=models.IntegerField(default=0,verbose_name="排序")
    intro = models.CharField(max_length=256,verbose_name="标签简介")
    class Meta:
        db_table='ask_lables'
        verbose_name="标签"
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name

class LabelFocus(BaseModel):
    label = models.ForeignKey(AskLables,verbose_name='关注的标签',on_delete=models.PROTECT, related_name='label')
    user = models.ForeignKey(User,verbose_name='关注的用户',on_delete=models.PROTECT)

    class Meta:
        db_table='label_focus'
        verbose_name="标签关注"
        verbose_name_plural=verbose_name

class Questions(BaseModel):
    # id=models.()
    label=models.ForeignKey(AskLables,on_delete=models.CASCADE,verbose_name="标签")
    title=models.CharField(max_length=128,verbose_name="标题")
    detail=models.TextField(verbose_name="问题详情")
    answers_count=models.IntegerField(verbose_name="回答数", default=0)
    author=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="作者")
    useful_count = models.IntegerField(verbose_name="有用数", default=0)
    click_count=models.IntegerField(verbose_name="点击量", default=0)
    status=models.SmallIntegerField(verbose_name="状态", default=0)

    class Meta:
        db_table='questions'
        verbose_name="问题"
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.title


class QuestionUseful(BaseModel):
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="用户")
    questions=models.ForeignKey(Questions,on_delete=models.CASCADE,verbose_name="问题")
    class Meta:
        db_table="question_useful"
        verbose_name="问题有用"
        verbose_name_plural=verbose_name


class Answers(BaseModel):
    question=models.ForeignKey(Questions,on_delete=models.CASCADE,verbose_name="回答的问题")
    content=models.TextField(verbose_name="回答的评论内容")
    useful_count=models.IntegerField(verbose_name="回答点赞数")
    author=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="回答人")
    status=models.SmallIntegerField(verbose_name="状态", default=0)
    useful_count = models.IntegerField(verbose_name='回答有用',default=0)

    class Meta:
        db_table="answers"
        verbose_name="我的回答"
        verbose_name_plural=verbose_name


class AnswersUseful(BaseModel):
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="用户")
    answer=models.ForeignKey(Answers,on_delete=models.CASCADE,verbose_name="有用的回答")

    class Meta:
        db_table='answers_useful'
        verbose_name="回答有用"
        verbose_name_plural=verbose_name


class AnswersComments(BaseModel):
    user=models.ForeignKey(User,verbose_name="评论用户")
    answer=models.ForeignKey(Answers,verbose_name="评论的回答")
    parent=models.ForeignKey("self",verbose_name="评论的父类", null=True, default=None)
    content=models.CharField(max_length=128,verbose_name="评论内容")
    status=models.SmallIntegerField(verbose_name="状态", default=0)

    class Meta:
        db_table='answers_comments'
        verbose_name="用户评论"
        verbose_name_plural=verbose_name
