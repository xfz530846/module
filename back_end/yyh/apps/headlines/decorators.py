from rest_framework import status
from rest_framework.response import Response


# request.data不可修改
def add_user_to_data(fun):
    """
    给request.data上添加　user 信息
    :param fun:
    :return:
    """
    def wrapper(request, *args, **kwargs):
        if request.user:
            request.data.update({'user': request.user})
        try:
            response = fun(request, *args, **kwargs)
        except Exception:
            return Response({'message': '收藏失败'}, status=status.HTTP_400_BAD_REQUEST)

        response.data = {'message': '收藏成功'}

        return response

    return wrapper


def after_collection_view(fun):

    def wrapper(request, *args, **kwargs):
        try:
            fun(request, *args, **kwargs)
        except Exception:
            return Response({'message': '失败'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': '成功'})

    return wrapper


