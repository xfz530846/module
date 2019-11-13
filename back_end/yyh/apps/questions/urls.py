from django.conf.urls import url

from . import views

urlpatterns=[
    url(r'^questions/$',views.QuestionsView.as_view()),
    url(r'^qa_categories/$',views.AskLablesView.as_view()),
    url(r'^qa_category/$',views.LableView.as_view()),
    url(r'^label_focus/$',views.LabelFocusView.as_view()),
    url(r'^label_unfocus/(?P<pk>\d+)/$', views.LabelUnfocusView.as_view()),
    url(r'^questions/(?P<pk>\d+)/$',views.QuestionDetailView.as_view()),
    url(r'^questions/(?P<pk>\d+)/answers/$',views.AnswersView.as_view()),
    url(r'^questions/useful/$',views.QuestionUsefulView.as_view()),
    url(r'^questions/(?P<pk>\d+)/useful/$',views.QuestionUnusefulView.as_view()),
    url(r'^answers/useful/$',views.AnswerUsefulView.as_view()),
    url(r'^answers/(?P<pk>\d+)/useful/$',views.AnswerUnusefulView.as_view()),
    url(r'^questions/useranswer/$', views.UserAnswersView.as_view()),
    url(r'^questions/usercomment/$', views.UserCommentView.as_view()),
    url(r'^questions/submit/$', views.QuestionsSubimtView.as_view()),
]