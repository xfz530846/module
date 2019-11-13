from django.http import JsonResponse
from rest_framework import exceptions
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication


class ImageJWTAuthentication(BaseJSONWebTokenAuthentication):

    def get_jwt_value(self, request):

        return request.GET.get('token', None)


def login_required(fun):
    """上传图片验证"""

    def warpper(request, *args, **kwargs):

        try:
            authentor = ImageJWTAuthentication()
            result = authentor.authenticate(request)
        except exceptions.AuthenticationFailed:
            return JsonResponse({"message": '请登陆后上传图片'}, status=401)

        if not result:
            return JsonResponse({"message": '请登陆后上传图片'}, status=401)

        return fun(request, *args, **kwargs)
    return warpper