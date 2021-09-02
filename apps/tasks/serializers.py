# _*_ coding: utf-8 _*_
# _*_ author_by zn _*_

from rest_framework import serializers
from .models import Tasks


class TaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=100)
    creator = serializers.CharField(required=False)
    app_name = serializers.CharField(required=False,
                                     source="app_id.app_name")
    playbook = serializers.CharField(required=True, max_length=1024)
    born = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    last = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = Tasks
        fields = "__all__"

    # def create(self, validated_data):
    #     """
    #     Create and return a new `Snippet` instance, given the validated data.
    #     """
    #     return Tasks.objects.create(**validated_data)
