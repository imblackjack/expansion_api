from django.db import models

# from apps.projects.models import Projects


# Create your models here.
class Tasks(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False, unique=True, verbose_name="任务名称")
    creator = models.CharField(max_length=32, null=True, blank=True, default='', verbose_name="创建者")
    app_id = models.ForeignKey("projects.Projects", on_delete=models.CASCADE, null=False, blank=False, verbose_name="关联应用")
    playbook = models.CharField(max_length=1024, null=False, blank=False, verbose_name="关联playbook")
    born = models.DateTimeField(max_length=32, null=True, blank=True, auto_now_add=True, verbose_name="创建时间")
    last = models.DateTimeField(max_length=32, null=True, blank=True, auto_now=True, verbose_name="上次执行时间")

    class Meta:
        verbose_name = '任务列表'
        verbose_name_plural = verbose_name

    # def __str__(self):
    #     return f"{self.id} {self.name}"


