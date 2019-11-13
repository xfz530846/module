from rest_framework import serializers
from questions.models import Questions, AskLables, Answers, AnswersComments, QuestionUseful, AnswersUseful, LabelFocus

# 问题详情显示
from users.models import User
from questions.models import Questions, AskLables, Answers, AnswersComments, AnswersUseful
from users.models import User



class QuestionDetailSerializer(serializers.ModelSerializer):
    current_time = serializers.DateTimeField(read_only=True)
    useful_status = serializers.IntegerField(read_only=True)

    class Meta:
        model = Questions
        fields = ('id', 'detail', 'answers_count', 'useful_count',
                  'useful_status', 'current_time', 'title', 'create_time',
                  'click_count', 'label', 'author')
        depth = 1


class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = ("id", "title", "author", "create_time", "useful_count", "answers_count", "click_count", "label")
        depth = 1

# 回答显示

class AskLablesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AskLables
        fields = '__all__'

class LabelFocusSerializer(serializers.ModelSerializer):

    class Meta:
        model = LabelFocus
        fields =('id', 'label')

    def validate(self, attrs):

        # 添加用户去保存数据
        user = self.context['request'].user
        if user and user.is_authenticated:
            attrs['user'] = user

        return attrs



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "nickname", "avatar_url")


class AnswersCommentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnswersComments
        fields = ("id", "answer", "content", "parent")


class AnswersSerializer(serializers.ModelSerializer):

    author = UserSerializer(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)
    useful_status = serializers.IntegerField(read_only=True)
    current_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model=Answers
        fields= ("id", "content", "useful_status", "useful_count", "current_time", "author", "comments")

    def get_comments(self, instance):

        if instance.answerscomments_set:
            query = instance.answerscomments_set.all().order_by('-create_time')

            return AnswersCommentsSerializer(query, many=True).data

        return ""


# 问题点赞

class QuestionUsefulSerializer(serializers.ModelSerializer):
    """问题点赞"""

    class Meta:
        model = QuestionUseful
        fields = ('id', 'questions')
        extra_kwargs = {
            'questions': {'write_only': True},
        }

    def validate(self, attrs):

        # 添加用户去保存数据
        user = self.context['request'].user
        if user and user.is_authenticated:
            attrs['user'] = user

        return attrs


# 答案点赞

class AnswerUsefulSerializer(serializers.ModelSerializer):
    """答案点赞"""

    class Meta:
        model = AnswersUseful
        fields = ('id', 'answer')
        extra_kwargs = {
            'answer': {'write_only': True},
        }

    def validate(self, attrs):

        # 添加用户去保存数据
        user = self.context['request'].user
        if user and user.is_authenticated:
            attrs['user'] = user

        return attrs



class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','nickname','avatar_url')

class UserAnswersSerializer(serializers.ModelSerializer):
    author=AuthorSerializer(read_only=True)
    class Meta:
        model=Answers
        fields=('id','question','content','author','useful_count')
        extra_kwargs = {
            "useful_count":{'read_only':True}
        }

    def validate(self, attrs):

        user = self.context['request'].user

        if user.is_authenticated:

            attrs['author'] = user

        return attrs


class UserCommentSerializer(serializers.ModelSerializer):
    user=AuthorSerializer(read_only=True)
    class Meta:
        model=AnswersComments
        fields=('id','user','content','answer','parent')
        

    def validate(self, attrs):

        user = self.context['request'].user

        if user.is_authenticated:

            attrs['user'] = user

        return attrs


class QuestionCreateSerializer(serializers.ModelSerializer):
    """问题发布"""

    class Meta:
        model = Questions
        fields = ("id", "title", "detail", "label", "answers_count", "author")
        extra_kwargs = {
            "title": {"max_length": 30},
            "answers_count": {"required": False, "read_only": True},
            "author": {"read_only": True}
        }

    def validate(self, attrs):

        user = self.context['request'].user
        attrs["author"] = user
        attrs["answers_count"] = 0

        return attrs
