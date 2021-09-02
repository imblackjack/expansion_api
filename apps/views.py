# _*_ coding: utf-8 _*_
# _*_ author_by zn _*


from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json

from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def index(request):
    return JsonResponse({
        "code": 0,
        "msg": "HelloWorld"
    })


# userRegister 用户注册
def userRegister(request):
    if request.method == "POST":
        body = json.loads(request.body)
        username = body.get("username", "")
        password = body.get("password", "")
        email = body.get("email", "")

        if username == "" or password == "" or email == "":
            return JsonResponse({
                "code": 40001,
                "msg": "输入的数据不合法"
            })

        User.objects.create_user(username=username, password=password, email=email)
        return JsonResponse({
            "code": 0,
            "msg": "创建用户成功"
        })

    return JsonResponse({
        "code": 0
    })


# userLogin 用户登录
def userLogin(request):
    if request.method == "GET":
        return HttpResponse("登录页面")

    if request.method == "POST":
        body = json.loads(request.body)
        username = body.get("username", "")
        password = body.get("password", "")

        if username == "" or password == "":
            return JsonResponse({
                "code": 40001,
                "msg": "输入的数据不合法"
            })

        user = auth.authenticate(request=request, username=username, password=password)

        # 判断用户名密码是否正确
        if user is not None:

            # 登录
            auth.login(request, user)

            return JsonResponse({
                "code": 0,
                "msg": "登录成功"
            })
        else:
            return JsonResponse({
                "code": 40002,
                "msg": "用户名或密码错误"
            })
    return JsonResponse({
        "code": 0,
    })


@login_required(login_url="/user/login")
def userMe(request):
    user = request.user
    username = user.get_username()
    email = user.email
    return JsonResponse({
        "code": 0,
        "data": {
            "username": username,
            "email": email
        }
    })


def userLogout(request):
    auth.logout(request)

    return JsonResponse({
        "code": 0,
        "msg": "注销成功"
    })
