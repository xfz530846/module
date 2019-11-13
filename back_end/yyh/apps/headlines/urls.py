from django.conf.urls import url

from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^headlines/$', views.HeadlinesListView.as_view()),
    url(r'^carousels/$', views.CarouselsView.as_view()),
    url(r'^headlines/(?P<category_id>\d+)/$', views.HeadlinesCreate.as_view()),
    url(r'^headline/categories/$', views.CategoryView.as_view()),
    url(r'^headlines/(?P<pk>\d+)/comments/$', views.HeadlinesCommentsView.as_view()),
    url(r'^headlines/(?P<pk>\d+)/detail/$',views.HeadlinesDetailView.as_view()),
    url(r'^headlines/collections/$',views.HeadlinesCollectionView.as_view()),
    url(r'^headlines/(?P<pk>\d+)/collections/$',views.HeadlinesUncollectionView.as_view()),
    url(r'^headlines/comments/$',views.HeadlinesCommentView.as_view()), # 发表评论
    url(r'^user/follow/$',views.UserAttentionView.as_view()), # 关注用户
    url(r'^user/(?P<pk>\d+)/follow/$',views.UserUnattentionView.as_view()), # 取消关注用户
    url(r'broswing_hitory/$', views.BroswingHistoryView.as_view()),  # 浏览记录 get
    url(r'^headlines/(?P<category_id>\d+)/hot/$',views.HeadlineHotView.as_view()), # 热门头条
    url(r'^headlines/labels/$',views.LabelsView.as_view()), # 标签显示
    url(r'^questions/hot/$',views.QuestionsHotView.as_view()), # 热门问题
    url(r'^talks/hot/$',views.TalkHotView.as_view()), # 热门吐槽
]