# _*_ coding: utf-8 _*_
# _*_ author_by zn _*_


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import status
from .models import Tasks
from apps.projects.models import Projects
from .serializers import TaskSerializer
from .pagination import PaginationSta
from rest_framework.views import APIView
from rest_framework.response import Response
from apis.playbook import PlayBookApi


class RunPlay(APIView):
    def post(self, request, *args, **kwargs):
        post_map = self.request.data
        app_id = post_map['app_id']
        # playbook str
        playbook = post_map['playbook']
        # name str
        name = post_map['name']
        # create play file
        file_path = '/opt/ansible/Ep/'
        file_name = name + '.yaml'

        with open(file_path + file_name, mode='w', encoding='utf-8') as f:
            f.write(playbook + '\n')

        if 'app_id' in post_map:
            obj = Projects.objects.get(id=app_id)

            # ansible hosts
            hosts = obj.ip.split('\n')
            print(hosts)

            _playbook_path = file_path + file_name
            playbook_path = [_playbook_path]
            play_run = PlayBookApi(playbook_path=playbook_path, hosts=hosts)
            data = play_run.playbookrun()
            print(data)

            return Response(data, status=status.HTTP_200_OK)

        else:
            return Response(1, status=status.HTTP_400_BAD_REQUEST)


class TaskViewSet(viewsets.ModelViewSet):
    """
        扩容任务管理
    """
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer
    pagination_class = PaginationSta
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'creator', 'playbook']
    ordering_fields = ['-last']


