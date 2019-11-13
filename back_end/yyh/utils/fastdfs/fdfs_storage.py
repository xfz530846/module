from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from fdfs_client.client import Fdfs_client


@deconstructible
class FastDFSStorage(Storage):

    def __init__(self):
        # 从配置信息中获取参数FDFS_URL对应的值
        if hasattr(settings, 'FDFS_URL'):
            self.base_url = settings.FDFS_URL
        else:
            raise ImproperlyConfigured("请配置FDFS_URL为Traker的地址")
        # 从配置信息中获取参数FDFS_CLIENT_CONF对应的值
        if hasattr(settings, 'FDFS_CLIENT_CONF'):
            self.client_conf = settings.FDFS_CLIENT_CONF
        else:
            raise ImproperlyConfigured('请配置FDFS_CLIENT_CONF为config文件路径的地址')
        # 创建Fdfs_client 对象
        self.client = Fdfs_client(self.client_conf)

    # def __init__(self, base_url=None, client_conf=None):
    #     """
    #     初始化
    #     :param base_url: 用于构造图片完整路径使用,图片服务器的域名
    #     :param client_conf:FastDFS客户端配置文件的路径
    #     """
    #     if base_url is None:
    #         base_url = settings.FDFS_URL
    #     self.base_url = base_url
    #
    #     if client_conf is None:
    #         client_conf = settings.FDFS_CLIENT_CONF
    #     self.client_conf = client_conf
    #     self.client = Fdfs_client(self.client_conf)

    def _open(self):
        """
        永不打开文件,所以省略
        :return:
        """
        pass

    def _save(self, name, content):
        """
        在FastDFS中保存文件
        :param name:  传入的文件名
        :param content: 文件内容
        :return: 保存到数据库中的FastDFS文件名
        """

        ext_name = name.split('.')[-1]

        ret = self.client.upload_appender_by_buffer(content.read(), ext_name)
        if ret.get('Status') != 'Upload successed.':
            raise Exception('Upload file failed')
        file_name = ret.get('Remote file_id')

        return file_name

    def url(self, name):
        """
        返回文件的完整路径
        :param name: 数据库中保存的文件名
        :return: 返回的是完整的url路径
        """
        print(self.base_url + name)
        return self.base_url + name

    def exists(self, name):
        """
        判断文件是否存在,FastDFS可以自行解决文件的重名问题,
        所以此处返回false,告诉django上传的都是心文件
        :param name: 文件名
        :return: False
        """
        return False