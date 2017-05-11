# -*- coding: utf-8 -*-
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render
from models import User, Article
from django.http import HttpResponse, JsonResponse
import json
from markdown import markdown
from django.core import serializers
# from markdown import markdown
# Create your views here.
import sys

reload(sys)
sys.setdefaultencoding('utf-8')  # 解决编码问题


# api接口书写
# 注册api
def signup(request):
    # 检察用户名是否为空
    # 检察密码是否为空
    # 检察用户名是否存在
    # 加密密码
    # 存入数据库

    if not has_username_password_email(request):
        register_check_json = {
            "status": 0,
            "msg": "用户名,密码,邮箱都不能为空"
        }
        return JsonResponse(register_check_json)
    else:
        username = has_username_password_email(request)[1]
        password = has_username_password_email(request)[2]
        email = has_username_password_email(request)[3]
        hash_password = make_password(password)
        assume_permission = 1

        boolen_result = User.objects.filter(auth=username).exists()
        if boolen_result:
            return JsonResponse({"status": 0, "msg": "name is exists"})
        try:
            result = User.objects.get_or_create(auth=username, pwd=hash_password, email=email,
                                                permission=assume_permission)
            if result[1]:
                info_json = {
                    "status": 1,
                    "msg": "用户名密码可以注册!",
                    "username": username,
                }
                return JsonResponse(info_json)
        except KeyError:
            register_except_json = {
                "status": 0,
                "msg": "用户名重复"
            }
            return JsonResponse(register_except_json)


# 登录api
def login(request):
    # 检察是否为空
    if not has_username_and_password(request, null=None):
        login_check_json = {
            "status": 0,
            "msg": "用户名或密码不能为空"
        }
        return JsonResponse(login_check_json)
    else:
        username = has_username_and_password(request)[1]
        password = has_username_and_password(request)[2]
        boolen_result = User.objects.filter(auth=username).exists()
        # 检察是否存在
        if not boolen_result:
            user_not_json = {
                "status": 0,
                "msg": "用户名不存在!",
                "username": username,
                "password": password

            }
            return JsonResponse(user_not_json)
        else:
            # 检察密码是否正确
            query_password_result = User.objects.get(auth=username).pwd
            if not check_password(password, query_password_result):
                # print check_password(password, query_password_result)
                return JsonResponse({"status": 0, "msg": "password error!"})
            else:
                # 把用户名和ID写入session
                user_id = User.objects.get(auth=username).id
                request.session['username'] = username
                request.session['user_id'] = user_id

                password_ok_json = {
                    "status": 1,
                    "msg": "用户名密码正确",
                    "username": username,
                    "password": password,
                    "user_id": request.session['user_id']

                }
                return JsonResponse(password_ok_json)


# 登出api
def logout(request):
    # 检察是否为空
    if not has_username_and_password(request, null=None):
        login_check_json = {
            "status": 0,
            "msg": "用户名或密码不能为空"
        }
        return JsonResponse(login_check_json)
    else:
        if not is_logged_in(request):
            logout_json = {
                "status": 0,
                "msg": "用户已经登出，不可以重复!"
            }
            return JsonResponse(logout_json)
        else:
            try:
                # 不存在时报错
                del request.session['user_id']
                del request.session['username']
            except KeyError:
                pass
            logout_json = {
                "status": 1,
                "msg": "登出成功!"
            }
            return JsonResponse(logout_json)


# 判断注册用户是否有用户名 密码 邮箱
def has_username_password_email(request, null=None):
    received_json_data = json.loads(request.body)
    username = received_json_data['username']
    password = received_json_data['password']
    email = received_json_data['password']
    print username, password, email
    if username == null or password == null or email == null:
        return False
    return True, username, password, email


# 判断用户名密码是否为空
def has_username_and_password(request, null=None):
    received_json_data = json.loads(request.body)
    username = received_json_data['username']
    password = received_json_data['password']
    # username = username.encode("utf-8")
    # username = unicode(username, "utf-8")
    if len(username) == 0 or len(password) == 0:
        return False
    return True, username, password


# 检测用户是否登录
def is_logged_in(request):
    # 如果session中存在user_id就返回，没有返回False
    if request.session.get('user_id', default=None) is None:
        return False
    return True, request.session.get('user_id')


# request 判断请求中是否有某个关键字
def rq(request, key):
    if request.method == 'POST':
        if request.POST.get(key, None) is None:
            return False
        else:
            return request.POST.get(key)
    if request.method == 'GET':
        if request.GET.get(key, None) is None:
            return False
        else:
            return request.GET.get(key)
    return False


def article_data(request):
    response_list = dict()
    response_json = dict()
    data = serializers.serialize("json", Article.objects.all())
    json_data = json.loads(data)
    for i in json_data:
        response_data = dict()
        response_data['id'] = i['pk']
        response_data['author_id'] = i['fields']['auth_id']
        response_data['category'] = i['fields']['category']
        response_data['title'] = i['fields']['title']
        response_data['content'] = i['fields']['content'][0:168]
        response_data['pub_date'] = i['fields']['pub_date'].split('T')[0]
        response_list[i['pk']] = response_data
    response_json['status'] = 1
    response_json['data'] = response_list
    return HttpResponse(json.dumps(response_json))


def index(request):
    if request.method == 'POST':
        response_list = []
        response_json = dict()
        data = serializers.serialize("json", Article.objects.all())
        json_data = json.loads(data)
        for i in json_data:
            response_data = dict()
            response_data['id'] = i['pk']
            response_data['author_name'] = i['fields']['auth_name']
            response_data['author_id'] = i['fields']['auth_id']
            response_data['category'] = i['fields']['category']
            response_data['title'] = i['fields']['title']
            response_data['content'] = i['fields']['content'][0:168]
            response_data['pub_date'] = i['fields']['pub_date'].split('T')[0]
            response_list.append(response_data)
        response_json['data'] = response_list
        return HttpResponse(json.dumps(response_json))
    elif request.method == 'GET':
        return render(request, 'index.html')


def publish(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body)
        author_id = received_json_data['author_id']
        category_str = received_json_data['category_str']
        print received_json_data['category_str']

        title = received_json_data['title']
        content = received_json_data['content']
        mark_content = markdown(content)
        Article_Result = Article.objects.create(category=category_str, title=title, auth_id_id=author_id,
                                                content=mark_content)
        return JsonResponse({'status': 1, 'msg': 'OK'})
    elif request.method == 'GET':
        return render(request, 'publish.html')


def article(request, request_id):
    data = serializers.serialize("json", Article.objects.filter(id=request_id))
    json_data = json.loads(data)
    print len(json_data)
    if len(json_data) >= 1:
        response_list = []
        response_json = dict()
        for i in json_data:
            response_data = dict()
            response_data['id'] = i['pk']
            response_data['author'] = i['fields']['auth_name']
            response_data['category'] = i['fields']['category']
            response_data['title'] = i['fields']['title']
            response_data['content'] = i['fields']['content']
            response_data['pub_date'] = i['fields']['pub_date'].split('T')[0]
            response_list.append(response_data)

        response_json['data'] = response_list
        return render(request, 'article.html', {'data': json.dumps(response_json)})

    else:
        return JsonResponse({"status": 1, "msg": "request error!"})


def aboutme(request):
    return render(request, 'aboutme.html')
