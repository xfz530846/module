from django.db import transaction
from django.db.models import F
from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from rest_framework import status

from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView,RetrieveAPIView, CreateAPIView
from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from headlines.serializers import CollectionSerializer
from questions import models
from questions.models import Questions, AskLables, QuestionUseful, Answers, AnswersUseful, LabelFocus
from questions.serializers import QuestionDetailSerializer, AnswersSerializer, QuestionUsefulSerializer, \
    AnswerUsefulSerializer, AskLablesSerializer, LabelFocusSerializer, QuestionCreateSerializer
from questions.models import Questions, AskLables, QuestionUseful, Answers
from questions.serializers import QuestionDetailSerializer, AnswersSerializer, UserAnswersSerializer, UserCommentSerializer,AnswerUsefulSerializer, AskLablesSerializer, LabelFocusSerializer
from questions.models import Questions, AskLables, QuestionUseful
from questions.serializers import QuestionDetailSerializer
from mlh.utils.pagination import StandardResultsSetPagination
from questions.models import Questions
from questions.serializers import QuestionsSerializer


class QuestionsView(ListAPIView):
    queryset = Questions.objects.all()
    serializer_class = QuestionsSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        order = self.request.query_params['order']
        filter = self.request.query_params['filter']
        category_id = self.request.query_params['category_id']

        if filter == 'wait':
            #等待回答
            queryset = self.queryset.filter(answers_count=0).order_by(order)

        elif category_id != '0' and not order:

            queryset = self.queryset.filter(label_id=category_id)

        elif category_id != '0' and  order:

            queryset = self.queryset.filter(label_id=category_id).order_by(order,'-create_time')

        else:
            queryset=self.queryset.order_by(order)


        return queryset

#获取标签列表
class AskLablesView(ListAPIView):

    serializer_class = AskLablesSerializer

    def get_queryset(self):
        queryset = AskLables.objects.all()
        order = self.request.query_params['order']
        if order!='':
            queryset = queryset.order_by(self.request.query_params['order'])

            return queryset
        else:
            return queryset

#获取标签
class LableView(APIView):
    def get(self,request):

        label_id = request.query_params["label_id"]
        user = request.user

        label = AskLables.objects.get(id=label_id)
        serializer = AskLablesSerializer(label)
        query_set = LabelFocus.objects.filter(user=user)

        label = serializer.data
        label['attention_status'] = 0
        for label_focus in query_set:
            if label['id'] == label_focus.label_id:
                label['attention_status'] = 1

        return Response(label,status=status.HTTP_200_OK)




class LabelFocusView(CreateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = LabelFocusSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)

        # 判断用户是否已经关注了
        try:
            LabelFocus.objects.get(user=request.user,label=serializer.validated_data['label'])
        except LabelFocus.DoesNotExist:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({'message': '关注成功'}, status=status.HTTP_201_CREATED, headers=headers)

        return Response({'message': '关注失败'}, status=status.HTTP_400_BAD_REQUEST)


class LabelUnfocusView(DestroyAPIView):

    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        try:
            label = AskLables.objects.get(id=self.kwargs.get('pk'))
            instance = LabelFocus.objects.get(user=user, label=label)
        except LabelFocus.DoesNotExist:
            return Response({'message': '取消关注失败'}, status=status.HTTP_400_BAD_REQUEST)
        except AskLables.DoesNotExist:
            return Response({'message': '取消关注失败'}, status=status.HTTP_400_BAD_REQUEST)

        return instance

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)

        if response.status_code == 204:
            response.data = {'message': '取消关注成功'}

        return response


# questions/(?P<pk>\d+)/
class QuestionDetailView(RetrieveAPIView):
    """问答详情页显示"""

    # queryset = Questions.objects.all()
    serializer_class =QuestionDetailSerializer

    def get_object(self):

        id = self.kwargs['pk']
        try:
            question = Questions.objects.get(id=id)
        except Questions.DoesNotExist:
            raise
        question.useful_status = 0

        user = self.request.user
        if user and user.is_authenticated:
            user_useful = QuestionUseful.objects.filter(user=user, questions=question)
            if user_useful:
                question.useful_status = 1

        current_time = timezone.now()
        question.current_time = current_time

        return question

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)

        if response.status_code == 200:
            Questions.objects.filter(id=self.kwargs['pk']).update(click_count=(F('click_count') + 1))

        return response


# r'questions/(?P<pk>\d+)/answers/'
class AnswersView(ListAPIView):
    """回答显示"""

    serializer_class = AnswersSerializer

    def get_queryset(self):
        question_id = self.kwargs['pk']
        queryset = Answers.objects.filter(question_id=question_id).order_by('-create_time')

        user = self.request.user
        current_time = timezone.now()
        for model in queryset:
            model.useful_status = 0
            if user and user.is_authenticated:
                user_useful = AnswersUseful.objects.filter(user=user, answer=model)
                if user_useful:
                    model.useful_status = 1

            model.current_time = current_time

        return queryset


# r'questions/useful/'
class QuestionUsefulView(CreateAPIView):
    """问题点赞"""

    permission_classes = [IsAuthenticated]
    serializer_class = QuestionUsefulSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 判断用户是否已经点赞了
        try:
            QuestionUseful.objects.get(user=request.user, questions=serializer.validated_data['questions'])
        except QuestionUseful.DoesNotExist:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({'message': '点赞成功'}, status=status.HTTP_201_CREATED, headers=headers)

        return Response({'message': '点赞失败'}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):

        with transaction.atomic():
            instance = serializer.save()
            Questions.objects.filter(id=instance.questions.id).update(useful_count=(F('useful_count') + 1))


# r'questions/{pk}/useful/'
class QuestionUnusefulView(DestroyAPIView):
    """问题取消点赞"""

    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        try:
            question = Questions.objects.get(id=self.kwargs.get('pk'))
            instance = QuestionUseful.objects.get(user=user, questions=question)
        except Questions.DoesNotExist:
            return Response({'message': '取消点赞失败'}, status=status.HTTP_400_BAD_REQUEST)
        except QuestionUseful.DoesNotExist:
            return Response({'message': '取消点赞失败'}, status=status.HTTP_400_BAD_REQUEST)

        return  instance

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)

        if response.status_code == 204:
            response.data = {'message': '取消点赞成功'}

        return response

    def perform_destroy(self, instance):

        with transaction.atomic():
            instance.delete()
            Questions.objects.filter(id=instance.questions.id).update(useful_count=(F('useful_count') - 1))


# r'answers/useful/'
class AnswerUsefulView(CreateAPIView):
    """答案点赞"""

    permission_classes = [IsAuthenticated]
    serializer_class = AnswerUsefulSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            AnswersUseful.objects.get(user=request.user, answer=serializer.validated_data['answer'])
        except AnswersUseful.DoesNotExist:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({'message': '点赞成功'}, status=status.HTTP_201_CREATED, headers=headers)

        return Response({'message': '点赞失败'}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):

        with transaction.atomic():
            instance = serializer.save()
            Answers.objects.filter(id=instance.answer.id).update(useful_count=(F('useful_count') + 1))


# r'answers/{pk}/useful/'
class AnswerUnusefulView(DestroyAPIView):
    """答案取消点赞"""

    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        try:
            answer = Answers.objects.get(id=self.kwargs.get('pk'))
            instance = AnswersUseful.objects.get(user=user, answer=answer)
        except Answers.DoesNotExist:
            return Response({'message': '取消点赞失败'}, status=status.HTTP_400_BAD_REQUEST)
        except AnswersUseful.DoesNotExist:
            return Response({'message': '取消点赞失败'}, status=status.HTTP_400_BAD_REQUEST)

        return instance

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)

        if response.status_code == 204:
            response.data = {'message': '取消点赞成功'}

        return response

    def perform_destroy(self, instance):

        with transaction.atomic():
            instance.delete()
            Answers.objects.filter(id=instance.answer.id).update(useful_count=(F('useful_count') - 1))


#用户回答
class UserAnswersView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserAnswersSerializer
    def create(self,request, *args, **kwargs):
        data = {
            "question": request.data.get('question'),
            "content": request.data.get('content')
        }
        serializer=self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers=self.get_success_headers(serializer.data)
        return Response(serializer.data,status.HTTP_201_CREATED, headers=headers)

    def perform_create(self,serializer):
        instance = serializer.save()
        Questions.objects.filter(id=instance.question.id).update(answers_count=(F('answers_count') + 1))



#用户评论
class UserCommentView(CreateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = UserCommentSerializer

    def create(self,request, *args, **kwargs):

        data = {
            "answer" : request.data.get('answer'),
            "content" : request.data.get('content'),
            'parent':request.data.get('parent')
        }

        serializer=self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers=self.get_success_headers(serializer.data)
        return Response(serializer.data,status.HTTP_201_CREATED, headers=headers)


# r''/questions/submit''
class QuestionsSubimtView(CreateAPIView):
    """问题发布"""

    permission_classes = [IsAuthenticated] 
    serializer_class = QuestionCreateSerializer




