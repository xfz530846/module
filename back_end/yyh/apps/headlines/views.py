import base64
import datetime
import pickle

from django.db import transaction
from django.db.models import F
from django.utils import timezone
from django_redis import get_redis_connection
from redis import StrictRedis
from rest_framework import status
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from headlines.models import Comments, HeadlinesCollections, BroswingHistory, HeadlinesLabel
from headlines.serializers import CommentCreateSerializer, AttentionSerializer, BroswingHistorySerializer, \
    LabelSerializer, QuestionsHotSerializer, TalkHotSerializer
from headlines.models import  Comments, HeadlinesCollections
from headlines.serializers import CommentCreateSerializer, AttentionSerializer, HeadlineHotSerializer
from headlines.serializers import HeadlinesDetailSerializer, HeadlinesCommentSerializer, CollectionSerializer
import re
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from headlines.models import Headlines, Categories, Carousel
from headlines.serializers import HeadlinesListSerializer, CarouselSerializer, CategorySerializer, \
    HeadlinesCreateSerializer
from headlines.utils import HeadlinesPagination
from questions.models import AskLables, Questions
from talks.models import Talk
from users.models import FansFollowed, User


# headline/categories/
class CategoryView(ListAPIView):
    """头条分类"""

    queryset = Categories.objects.filter(is_delete=0).order_by("sequence")
    serializer_class = CategorySerializer


# headlines/
class HeadlinesListView(ListAPIView):
    """头条列表"""

    pagination_class = HeadlinesPagination

    filter_backends = (OrderingFilter, )
    ordering = ("-create_time", "-click_counts")

    serializer_class = HeadlinesListSerializer

    def get_queryset(self):
        queryset = Headlines.objects.filter(is_delete=0, status=Headlines.NEWS_STATUS_ENUM["APPROVED"])
        try:
            # category_id = self.kwargs['category_id']
            category_id = self.request.query_params['category_id']  
            category = Categories.objects.get(id=category_id)
        except:
            return queryset

        return queryset.filter(category=category)

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset).select_related('author')

        user = self.request.user
        for model in queryset:
            re_obj = re.search(r'^<p>(.*)</p>', model.content)
            model.summary = model.content[302:600] + "..."
            model.attention_status = 0
            if user and user.is_authenticated:
                user_atten = FansFollowed.objects.filter(fans=user, followeds=model.author)
                if user_atten:
                    model.attention_status = 1

        return queryset


# r'headlines/(?P<category_id>)'
class HeadlinesCreate(CreateAPIView):
    """头条发布"""

    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]  
    serializer_class = HeadlinesCreateSerializer

    def create(self, request, *args, **kwargs):

        data = {
            "title": request.data.get('title'),
            "content": request.data.get('content'),
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):

        with transaction.atomic():
            headline = serializer.save()
            labels = self.request.data.get('labels')
            for label_id in labels:
                try:
                    label = AskLables.objects.get(id=label_id)
                except AskLables.DoesNotExist:
                    return Response({"message": "标签不存在"}, status=status.HTTP_400_BAD_REQUEST)

                HeadlinesLabel.objects.create(headline=headline, label=label)

# carousels/
class CarouselsView(ListAPIView):
    """轮播图显示"""

    queryset = Carousel.objects.filter(is_delete=0)
    serializer_class = CarouselSerializer


# headlines/(?P<pk>\d+)/detail/
class HeadlinesDetailView(RetrieveAPIView):
    """头条详情"""

    authentication_classes = [JSONWebTokenAuthentication]
    queryset = Headlines.objects.all()
    serializer_class = HeadlinesDetailSerializer

    def get_object(self):

        id = self.kwargs['pk']
        try:
            headline = Headlines.objects.get(id=id)
        except Headlines.DoesNotExist:
            raise
        headline.collection_status = 0
        headline.attention_status = 0
        user = self.request.user
        if user and user.is_authenticated:
            user_coll = HeadlinesCollections.objects.filter(user=user, headlines=headline)
            user_atten = FansFollowed.objects.filter(fans=user, followeds=headline.author)
            if user_coll:
                headline.collection_status = 1
            if user_atten:
                headline.attention_status = 1
            count = BroswingHistory.objects.filter(headlines=headline).count()
            if count == 1:
                broswing_history = BroswingHistory()
                broswing_history.headlines = headline
                broswing_history.user = user
                broswing_history.create_time = datetime.datetime.now()
                broswing_history.save()

        return headline

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)

        if response.status_code == 200:
            Headlines.objects.filter(id=self.kwargs['pk']).update(click_counts=(F('click_counts') + 1))

        return response


# r'headlines/comments/(?P<pk>\d+)'
class HeadlinesCommentsView(ListAPIView):
    """评论显示"""

    # queryset = Comments.objects.all()
    serializer_class = HeadlinesCommentSerializer

    def get_queryset(self):
        headlines_id = self.kwargs['pk']
        queryset = Comments.objects.filter(headlines_id=headlines_id).filter(parent=None).order_by('-create_time')

        return queryset


# r'headlines/collections/'
class HeadlinesCollectionView(CreateAPIView):
    """头条收藏"""
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CollectionSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            HeadlinesCollections.objects.get(user=request.user, headlines=serializer.validated_data['headlines'])
        except HeadlinesCollections.DoesNotExist:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({'message': '收藏成功'}, status=status.HTTP_201_CREATED, headers=headers)
        return Response({'message': '收藏失败'}, status=status.HTTP_400_BAD_REQUEST)


# r'headlines/{pk}/collections/'
class HeadlinesUncollectionView(DestroyAPIView):
    """头条取消收藏"""
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        try:
            headline = Headlines.objects.get(id=self.kwargs.get('pk'))
            instance = HeadlinesCollections.objects.get(user=user, headlines=headline)
        except Headlines.DoesNotExist:
            return Response({'message': '取消收藏失败'}, status=status.HTTP_400_BAD_REQUEST)
        except HeadlinesCollections.DoesNotExist:
            return Response({'message': '取消收藏失败'}, status=status.HTTP_400_BAD_REQUEST)

        return  instance

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)

        if response.status_code == 204:
            response.data = {'message': '取消收藏成功'}

        return response


# http://headlines/comments/
class HeadlinesCommentView(CreateAPIView):
    """头条评论"""

    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CommentCreateSerializer

    def create(self, request, *args, **kwargs):

        data = {
            "headlines": request.data.get('headlines'),
            "content": request.data.get('content')
        }

        # serializer = self.get_serializer(data=data, partial=True)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):

        with transaction.atomic():
            instance = serializer.save()
            if instance.parent:
                Comments.objects.filter(id=instance.parent.id).update(child_counts=(F('child_counts') + 1))
            Headlines.objects.filter(id=instance.headlines.id).update(comment_counts=(F('comment_counts') + 1))


# r'user/follow/'
class UserAttentionView(CreateAPIView):
    """用户关注"""

    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AttentionSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)

        try:
            FansFollowed.objects.get(fans=request.user, followeds=serializer.validated_data['followeds'])
        except FansFollowed.DoesNotExist:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({'message': '关注成功'}, status=status.HTTP_201_CREATED, headers=headers)

        return Response({'message': '关注失败'}, status=status.HTTP_400_BAD_REQUEST)


# r''user/{pk}/follow/'
class UserUnattentionView(DestroyAPIView):
    """用户取消关注"""
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        try:
            followed = User.objects.get(id=self.kwargs.get('pk'))
            instance = FansFollowed.objects.get(fans=user, followeds=followed)
        except FansFollowed.DoesNotExist:
            return Response({'message': '取消关注失败'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': '取消关注失败'}, status=status.HTTP_400_BAD_REQUEST)

        return instance

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)

        if response.status_code == 204:
            response.data = {'message': '取消关注成功'}

        return response


# r''headlines/\d+/hot/'
class HeadlineHotView(ListAPIView):
    """热门头条显示"""

    queryset = Headlines.objects.all()
    serializer_class = HeadlineHotSerializer


    def list(self, request, *args, **kwargs):

        category_id = self.kwargs["category_id"]

        redis_con = get_redis_connection('hot_headlines')
        data = redis_con.get('headline_{0}'.format(self.kwargs["category_id"]))

        if data:
            context = pickle.loads(base64.b64decode(data))
            return Response(context)
        else:
            try:
                Categories.objects.get(id=category_id)
            except Categories.DoesNotExist:
                return Response({'message': '参数错误'}, status=status.HTTP_400_BAD_REQUEST)

            dt = timezone.now() - timezone.timedelta(10)
            query = Headlines.objects.filter(category_id=category_id, is_delete=0, create_time__gt=dt).order_by(
                '-click_counts')
            serializer = self.get_serializer(query[:4], many=True)
            data = base64.b64encode(pickle.dumps(serializer.data)).decode()

            redis_con = get_redis_connection('hot_headlines')  # type: StrictRedis
            redis_con.set('headline_{0}'.format(self.kwargs["category_id"]), data)

            return Response(serializer.data)


# r''questions/hot/'
class QuestionsHotView(ListAPIView):
    """热门问题显示"""

    queryset = Questions.objects.all()
    serializer_class = QuestionsHotSerializer

    def list(self, request, *args, **kwargs):

        redis_con = get_redis_connection('hot_questions')
        data = redis_con.get('hot_questions')

        if data:
            context = pickle.loads(base64.b64decode(data))
            return Response(context)
        else:
            dt = timezone.now() - timezone.timedelta(10)
            query = Questions.objects.filter(is_delete=0, create_time__gt=dt).order_by(
                '-click_count')

            serializer = self.get_serializer(query[:5], many=True)
            data = base64.b64encode(pickle.dumps(serializer.data)).decode()
            redis_con = get_redis_connection('hot_questions')  # type: StrictRedis
            redis_con.set('hot_questions', data)

            return Response(serializer.data)

# r''talks/hot/'
class TalkHotView(ListAPIView):
    """热门问题显示"""

    queryset = Talk.objects.all()
    serializer_class = TalkHotSerializer

    def list(self, request, *args, **kwargs):

        redis_con = get_redis_connection('hot_talks')
        data = redis_con.get('hot_talks')

        if data:
            context = pickle.loads(base64.b64decode(data))
            return Response(context)
        else:

            dt = timezone.now() - timezone.timedelta(10)

            query = Talk.objects.filter(is_delete=0, create_time__gt=dt).order_by(
                '-like_count')

            serializer = self.get_serializer(query[:4], many=True)

            data = base64.b64encode(pickle.dumps(serializer.data)).decode()

            redis_con = get_redis_connection('hot_talks')  # type: StrictRedis
            redis_con.set('hot_talks', data)

            return Response(serializer.data)


# r'labels/'
class LabelsView(ListAPIView):
    queryset = AskLables.objects.order_by('sequence')
    serializer_class = LabelSerializer



class BroswingHistoryView(ListAPIView):
    """浏览记录"""
    serializer_class = BroswingHistorySerializer
    def get_queryset(self):
        broswing_history = BroswingHistory.objects.filter(user=self.request.user).order_by('-create_time')
        return broswing_history
