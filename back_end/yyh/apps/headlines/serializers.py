from rest_framework import serializers

from headlines.models import Headlines, Carousel, Categories, Comments, HeadlinesCollections, BroswingHistory
from questions.models import AskLables, Questions
from talks.models import Talk
from headlines.models import Headlines, Carousel, Categories, Comments, HeadlinesCollections,BroswingHistory
from users.models import User, FansFollowed


# 头条列表

class UserSerializer(serializers.ModelSerializer):
    """用户信息"""
    class Meta:
        model = User
        fields = ("id", "nickname", "avatar_url")


class HeadlinesListSerializer(serializers.ModelSerializer):
    """头条列表"""

    author = UserSerializer()
    summary = serializers.CharField(read_only=True)
    attention_status = serializers.IntegerField(read_only=True)

    class Meta:
        model = Headlines
        fields = ("id", "category", "title", "create_time", "summary", "attention_status", "author")


# 轮播图

class CarouselSerializer(serializers.ModelSerializer):
    """轮播图"""

    class Meta:
        model = Carousel
        fields = ("id", "image", "target", "sequence")


# 头条分类

class CategorySerializer(serializers.ModelSerializer):
    """头条分类"""

    class Meta:
        model = Categories
        fields = ("id", "name", "sequence")


# 头条发布

class HeadlinesCreateSerializer(serializers.ModelSerializer):
    """头条发布"""

    class Meta:
        model = Headlines
        # exclude = ("is_delete", "reason", "create_time", "update_time")
        fields = ("id", "category", "title", "content", "image", "comment_counts", "click_counts")
        read_only_fields = ("author", "category", "comment_counts", "click_counts", "status")
        extra_kwargs = {
            "title": {"max_length": 30}
        }

    def validate(self, attrs):

        try:
            category_id = self.context['view'].kwargs['category_id']  # 获取
            category = Categories.objects.get(id=category_id)
        except Categories.DoesNotExist:
            raise serializers.ValidationError("分类序号错误")

        user = self.context['request'].user

        attrs["category"] = category
        attrs["author"] = user

        return attrs


# 头条详情

class HeadlinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Headlines
        fields = ['id','title']


class UserAuthorSerializer(serializers.ModelSerializer):

    # headlines_set = HeadlinesSerializer(many=True)
    headlines = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'avatar_url','nickname','headlines']

    def get_headlines(self, obj):

        if obj.headlines_set.all():
            query = obj.headlines_set.all().order_by('-create_time')[:4]
            return HeadlinesSerializer(query, many=True).data
        return ''


class HeadlinesDetailSerializer(serializers.ModelSerializer):
    author = UserAuthorSerializer()
    collection_status = serializers.IntegerField(read_only=True)
    attention_status = serializers.IntegerField(read_only=True)

    class Meta:
        model = Headlines
        fields = ['collection_status',
                  'attention_status',
                  'title', 'content',
                  'image', 'comment_counts',
                  'create_time',
                  'id',
                  'category',
                  'author'
                  ]




# 头条收藏

class CollectionSerializer(serializers.ModelSerializer):
    """头条收藏"""

    class Meta:
        model = HeadlinesCollections
        fields = ('id', 'headlines')
        extra_kwargs = {
            'headlines': {'write_only': True},
        }

    def validate(self, attrs):

        # 添加用户去保存数据
        user = self.context['request'].user
        if user and user.is_authenticated:
            attrs['user'] = user

        return attrs


# 头条评论添加

class CommentCreateSerializer(serializers.ModelSerializer):
    """头条评论"""

    user = UserSerializer(read_only=True)

    class Meta:
        model = Comments
        fields = ('id', 'headlines', 'content', 'child_counts', 'parent', 'user')
        extra_kwargs = {
            'headlines': {'write_only': True},
            'child_counts': {'read_only': True},
            'parent': {'read_only': True},
        }
        # depth = 1

    def validate(self, attrs):

        # 添加用户和父评论id

        user = self.context['request'].user

        parent_id = self.context['request'].data.get('parent_id', None)

        if parent_id:
            try:
                parent_comment = Comments.objects.get(id = parent_id)
            except serializers.ValidationError('参数错误'):
                raise

            attrs['parent'] = parent_comment
        attrs['user'] = user

        return attrs


# 头条评论显示

class CommentsSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Comments
        fields = ('id', 'user', 'content')


class HeadlinesCommentSerializer(serializers.ModelSerializer):
    """头条评论"""

    user = UserSerializer()
    child_comments = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = ['id', 'user', 'content', 'child_counts', 'child_comments']

    def get_child_comments(self, obj):
        if obj.comments_set.all():
            query = obj.comments_set.all().order_by("-create_time")[0]
            return CommentsSerializer(query).data

        return ''


class AttentionSerializer(serializers.ModelSerializer):
    """头条收藏"""

    class Meta:
        model = FansFollowed
        fields = ('id', 'followeds')
        extra_kwargs = {
            'followeds': {'write_only': True},
        }

    def validate(self, attrs):

        # 添加用户去保存数据
        user = self.context['request'].user
        if user and user.is_authenticated:
            attrs['fans'] = user

        return attrs


class BroswingHistorySerializer(serializers.ModelSerializer):
    """浏览记录"""
    class Meta:
        model = BroswingHistory
        fields = '__all__'
        depth = 2



# 热门头条显示

class HeadlineHotSerializer(serializers.Serializer):
    """热门头条显示"""

    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(read_only=True)

# 热门问题显示

class QuestionsHotSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Questions
        fields = ("id", "title", "create_time","author")

# 热门吐槽显示

class TalkHotSerializer(serializers.ModelSerializer):

    class Meta:
        model = Talk
        fields = ("id", "detail")


# 标签显示

class LabelSerializer(serializers.ModelSerializer):
    """标签显示"""

    class Meta:
        model = AskLables
        fields = ("id", "name")
