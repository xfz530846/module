from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from . import views

urlpatterns = [
    url(r'^authorizations/$', obtain_jwt_token),
    url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
    url(r'mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
    url(r'register/$', views.UserCreateView.as_view()),
    url(r'user/$', views.UserInfoView.as_view()),#用户登录状态下的信息展示
    url(r'user_archive/$',views.UserArchivesView.as_view()),#查询user_archive对象是否存在 get
    url(r'user_center/$', views.UserDetailView.as_view()),#获取个人中心的数据 get
    url(r'my_answers/$', views.MyAnswersView.as_view()),#我的回答
    url(r'my_questions/$', views.MyQuestionsView.as_view()),#我的提问
    url(r'my_headlines/$', views.MyHeadLinesView.as_view()),#我的头条
    url(r'user_detail/$', views.CreateUserArchiveView.as_view()),#如果用户user_archive，创建一个user_archive  post
    url(r'my_file/$',views.MyFileView.as_view()),#个人中心点击详细档案发送请求 get
    url(r'collect_articles/$',views.MyCollectArticlasView.as_view()),#我收藏的文章 get
    url(r'collect_talks/$',views.MyCollectTalksView.as_view()),#我收藏的吐槽 get
    url(r'focus_question/$',views.FocusQuestionsView.as_view()),#我关注的问题 get
    url(r'edit_myfile/$',views.EditMyfileView.as_view()),#编辑个人档案 put
]
