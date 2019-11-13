from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from headlines.models import Headlines, HeadlinesCollections
from questions.models import Questions, Answers, QuestionUseful
from talks.models import UserTalkCollection
from users import serializers

from users.models import User, UserArchives, MyActive

from users.serializers import MyHeadLineSerializer,UserCenterSerializer, MyAnswerSerializer, MyQuestionSerializer, MyCollectArticlasSerializer, \
    MyCollectTalksSerializer, FocusQuestionsSerializer, MyActiveSerializer


class UsernameCountView(APIView):
    """
    用户名数量
    """

    def get(self, request, username):
        """
        获取指定用户名数量
        """
        count = User.objects.filter(username=username).count()

        data = {
            'username': username,
            'count': count
        }

        return Response(data)

#手机号是否注册检测
class MobileCountView(APIView):
    """
    手机号数量
    """

    def get(self, request, mobile):
        """
        获取指定手机号数量
        """
        count = User.objects.filter(mobile=mobile).count()

        data = {
            'mobile': mobile,
            'count': count
        }

        return Response(data)

#用户注册
class UserCreateView(CreateAPIView):
    """
    用户注册
    """
    serializer_class = serializers.CreateUserSerializer


#用户登录状态下的信息展示
class UserInfoView(APIView):

    authentication_classes = [JSONWebTokenAuthentication]

    def get(self,request):

        #获取request里面的user
        try:
            user = request.user
        except Exception:
            # 验证失败，用户未登录
            user = None

        if user:
            #如果有用户则将用户信息传上去
            user_info = {
                "nickname":user.nickname,
                "avatar_url": user.avatar_url
            }
            response = Response(user_info, status=status.HTTP_200_OK)
            return response
        else:
            #如果没有用户，则返回NONE
            return Response(None, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

# class UserArchivesView(APIView):
#
#
#     serializer_class = serializers.UserCenterSerializer
#     authentication_classes = [JSONWebTokenAuthentication]

class UserDetailView(APIView):
    """用户个人中心"""

    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        """查询个人中心user有没有对应的user_archive"""

        try:
            user = request.user
        except Exception:
            user = None
        if user:
            user_archive = UserArchives.objects.get(user = user)
            user_archive_serializer = UserCenterSerializer(user_archive)
            response = Response(user_archive_serializer.data,status=status.HTTP_200_OK)
        else:
            response = Response(None, status=status.HTTP_204_NO_CONTENT)
        return response


class UserArchivesView(APIView):
    """判断user_archive对象是否存在"""
    authentication_classes = [JSONWebTokenAuthentication]
    def get(self,request):
        count = UserArchives.objects.filter(user = request.user.id).count()
        return Response({'count':count})

class CreateUserArchiveView(APIView):
    """创建user_archive对象"""
    authentication_classes = [JSONWebTokenAuthentication]
    def post(self,request):
        user = request.user
        user_archive = UserArchives.objects.create(
            user = user
        )
        serializer = UserCenterSerializer(user_archive)
        return Response(serializer.data)


class MyAnswersView(ListAPIView):
    """我的回答"""


    serializer_class = MyAnswerSerializer

    def get_queryset(self):
        return Answers.objects.filter(author = self.request.user).order_by('-create_time')


class MyQuestionsView(ListAPIView):
    """我的提问"""
    serializer_class = MyQuestionSerializer

    def get_queryset(self):
        questions = Questions.objects.filter(author=self.request.user).order_by('-create_time')
        return questions


class MyHeadLinesView(ListAPIView):
    """我的头条"""
    serializer_class = MyHeadLineSerializer
    def get_queryset(self):
        headlines = Headlines.objects.filter(author=self.request.user).order_by('-create_time')
        return headlines


class MyCollectArticlasView(ListAPIView):
    """收藏的文章"""
    serializer_class = MyCollectArticlasSerializer
    def get_queryset(self):
        collect_articals = HeadlinesCollections.objects.filter(user = self.request.user).order_by('-create_time')
        return collect_articals


class MyCollectTalksView(ListAPIView):
    """收藏的吐槽"""
    serializer_class = MyCollectTalksSerializer
    def get_queryset(self):
        collect_talks = UserTalkCollection.objects.filter(user = self.request.user).order_by('-create_time')
        return collect_talks


class FocusQuestionsView(ListAPIView):
    """关注的问题"""
    serializer_class = FocusQuestionsSerializer
    def get_queryset(self):
        focus_question = QuestionUseful.objects.filter(user = self.request.user).order_by('-create_time')
        return focus_question


class MyFileView(APIView):
    """完整档案"""
    def get(self,request):
        user = request.user
        myfile = UserArchives.objects.get(user_id = user.id)
        serializer = UserCenterSerializer(myfile)
        return Response(serializer.data)


class MyActiveView(ListAPIView):
    """我的动态"""
    serializer_class = MyActiveSerializer
    def get_queryset(self):
        my_active = MyActive.objects.all().order_by('-create_time')
        return my_active


class EditMyfileView(APIView):


    def put(self,request):

        user = request.user
        user_archives = UserArchives.objects.get(user_id =user.id)
        serializer = UserCenterSerializer(user_archives, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data,status=status.HTTP_200_OK)


