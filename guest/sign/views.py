from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event


# Create your views here.
def index(request):
    return render(request,"index.html")

# 登录动作
def login_action(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        ####  未进行引用Django认证登录的模板 ####
        # if username == 'admin' and password == 'admin123':
        #     response = HttpResponseRedirect('/event_manage/')
        #     #response.set_cookie('user', username, 3600) # 添加浏览器cookie
        #     # 为了安全用session 替换掉cookie
        #     request.session['user'] = username # 将session信息记录到浏览器
        #     return response
        ######-------------------------------------#######
        if user is not None:
            auth.login(request, user) # 登录
            request.session['user'] = username
            response = HttpResponseRedirect('/event_manage/')
            return response
        else:
            return render(request, 'index.html', {'error': 'username or password error!'})

# 发布会管理
@login_required
def event_manage(request):
    event_list = Event.objects.all()
    # username = request.COOKIES.get('user', '') # 读取浏览器cookie
    username=request.session.get('user','') # 读取浏览器session
    return render(request, "event_manage.html", {"user":username,
                                                 "events":event_list})

# 发布会名称搜索
@login_required
def sreach_name(request):
    username = request.session.get('user', '')
    sreach_name = request.GET.get("name", "")
    event_list = Event.objects.filter(name__contains=sreach_name)
    return render(request, "event_manage.html", {"user":username,
                                                 "events": event_list})

