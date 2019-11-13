from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSSerializer, BadData
from users.models import User


class HeadlinesPagination(PageNumberPagination):
    """头条列表页分页"""

    page_size = 12
    page_size_query_param = "page_size"


def check_verify_token(token):
    """
    检查验证的token
    """
    serializer = TJWSSerializer(settings.SECRET_KEY)
    try:
        data = serializer.loads(token)
    except BadData:
        return None
    else:
        user_id = data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
        else:
            return user


def login_check(func):

    def wrapper(request, *args, **kwargs):
        token = request.GET.get('token',None)
        if not token:
            return JsonResponse({'message': '缺少token'}, status=status.HTTP_401_UNAUTHORIZED)

        # 验证token
        user = check_verify_token(token)
        if user is None:
            return JsonResponse({'message': '验证失败'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return func(request, *args, **kwargs)
    return wrapper
