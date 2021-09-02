# _*_ coding: utf-8 _*_
# _*_ author_by zn _*_

from rest_framework import serializers
from .models import Projects


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Projects
        fields = "__all__"
