# _*_ coding: utf-8 _*_
# _*_ author_by zn _*_

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework import filters
from .models import Projects
from .serializers import ProjectSerializer
from .pagination import PaginationSta
from rest_framework.views import APIView
from rest_framework.response import Response
from apis.paramiko import TransferApi
from apis.paramiko import CommandApi

from tools.logger import logger
import logging


class TransCode(APIView):
    """
        从前端传入ip port path等信息调用TransferApi下载文件
    """
    def post(self, request, *args, **kwargs):
        post_map = self.request.data

        source = post_map['source']
        s_port = post_map['s_port']
        s_port = int(s_port)
        s_code = post_map['s_code']

        # 配置本地代码路径
        l_code = '/tmp/a'

        username = 'root'

        transfer_run = TransferApi(source=source, s_port=s_port, s_code=s_code, l_code=l_code, username=username)
        ret = transfer_run.transfer()
        return Response(ret, status=status.HTTP_200_OK)

    """
        当下载动作完成时，根据app的id更新下载状态，前端展示完成百分比
    """
    def put(self, request, *args, **kwargs):

        print(request.stream.path)
        _path = request.stream.path
        _path_list = _path.split('/')
        print(_path_list)
        aid = int(_path_list[-2])

        project = Projects.objects.get(id=aid)

        put_map = request.data
        print(put_map)
        serializer = ProjectSerializer(instance=project, data=put_map)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RunCommand(APIView):
    """
        从前端传入ip port username password 等信息调用 CommandApi 执行 shell 命令
    """
    @logger(level=logging.INFO, message='post command_run api')
    def post(self, request, *args, **kwargs):
        post_map = self.request.data
        source = post_map['source']
        s_port = 22
        username = 'root'
        password = 'xxxxxx'

        command_run = CommandApi(source=source, s_port=s_port, username=username, password=password)

        shell_command = 'df -h'
        ret = command_run.command(shell_command)

        return Response(ret, status=status.HTTP_200_OK)


class ProjectViewSet(viewsets.ModelViewSet):
    """
        应用管理
    """
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = PaginationSta
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['app_name', 'did']
    ordering_fields = ['-id']



