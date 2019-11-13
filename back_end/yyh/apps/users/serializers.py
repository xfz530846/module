import re
from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from headlines.models import Headlines, HeadlinesCollections
from questions.models import Questions, Answers, QuestionUseful
from questions.serializers import QuestionDetailSerializer
from talks.models import UserTalkCollection
from users.models import User, UserArchives, MyActive


class CreateUserSerializer(serializers.ModelSerializer):
    """
    创建用户序列化器
    """
    sms_code = serializers.CharField(label='短信验证码', write_only=True)
    allow = serializers.CharField(label='同意协议', write_only=True)
    token = serializers.CharField(label='登录状态token', read_only=True)  # 增加token字段

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'sms_code', 'mobile', 'allow','token')
        extra_kwargs = {
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }

    def validate_mobile(self, value):
        """验证手机号"""
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式错误')
        return value

    def validate_allow(self, value):
        """检验用户是否同意协议"""
        if value != 'true':
            raise serializers.ValidationError('请同意用户协议')
        return value

    def validate(self, data):
        # 判断短信验证码
        redis_conn = get_redis_connection('verify_codes')
        mobile = data['mobile']
        real_sms_code = redis_conn.get('sms_%s' % mobile)
        if real_sms_code is None:
            raise serializers.ValidationError('无效的短信验证码')
        if data['sms_code'] != real_sms_code.decode():
            raise serializers.ValidationError('短信验证码错误')

        return data

    def create(self, validated_data):
        """
        创建用户
        """
        # 移除模型类中不存在的属性
        del validated_data['sms_code']
        del validated_data['allow']
        user = super().create(validated_data)

        user.set_password(validated_data['password'])
        user.nickname = validated_data['username']
        user.save()

        # 补充生成记录登录状态的token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token
        return user


class UserCenterSerializer(serializers.ModelSerializer):
    """个人中心序列化器"""

    class Meta:
        model = UserArchives
        fields = '__all__'
        depth = 1

    def validate_real_mobile(self, value):
        """验证手机号"""
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式错误')
        return value



class MyAnswerSerializer(serializers.ModelSerializer):
    question = QuestionDetailSerializer()
    class Meta:
        model = Answers
        fields = ['question','create_time','useful_count',]


class MyQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = ['id','title','create_time','useful_count',]


class MyHeadLineSerializer(serializers.ModelSerializer):
    """我的头条"""
    class Meta:
        model = Headlines
        fields = ['id','title','create_time','click_counts']
        read_only_fields = ['id']


class MyCollectArticlasSerializer(serializers.ModelSerializer):
    """收藏的文章"""
    class Meta:
        model = HeadlinesCollections
        fields = '__all__'
        depth = 2


class MyCollectTalksSerializer(serializers.ModelSerializer):
    """收藏的吐槽"""
    class Meta:
        model = UserTalkCollection
        fields = '__all__'
        depth = 2


class FocusQuestionsSerializer(serializers.ModelSerializer):
    """关注的问题"""
    class Meta:
        model = QuestionUseful
        fields = '__all__'
        depth = 2


class MyActiveSerializer(serializers.ModelSerializer):
    """我的动态"""
    class Meta:
        model = MyActive
        fields = '__all__'
        depth = 2


