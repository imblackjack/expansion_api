# Generated by Django 3.1.2 on 2021-08-13 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20210813_1152'),
    ]

    operations = [
        migrations.AddField(
            model_name='projects',
            name='code_status',
            field=models.IntegerField(blank=True, default=0, max_length=32, null=True, verbose_name='下载代码状态'),
        ),
    ]