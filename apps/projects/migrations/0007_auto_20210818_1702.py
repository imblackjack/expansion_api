# Generated by Django 3.1.2 on 2021-08-18 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_projects_code_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='s_code',
            field=models.CharField(blank=True, default='', max_length=1024, null=True, verbose_name='源代码path'),
        ),
    ]
