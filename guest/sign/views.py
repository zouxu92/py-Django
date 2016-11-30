from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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

# 嘉宾管理
@login_required
def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 没有页码返回首页
        contacts = paginator.page(1)
    except EmptyPage:
        # 当前页面数大于最大页码数,返回最后一页数据
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username,
                                                 "guests": contacts})

# 嘉宾电话搜索
@login_required
def sreach_phone(request):
    username = request.session.get('user', '')
    sreach_phone = request.GET.get("phone", "")
    guest_list = Guest.objects.filter(phone__contains=sreach_phone)
    return render(request, "guest_manage.html", {"user": username,
                                                 "guests": guest_list})

# 签到页面
@login_required
def sign_index(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    # 已签到数
    already_count = Guest.objects.filter(event_id=event_id).filter(sign=1).count()
    # 当前发布会嘉宾数
    total_count = Guest.objects.filter(event_id=event_id).count()
    return render(request, 'sign_index.html', {'event': event,
                                               'total_count': total_count,
                                               'already_count': already_count})

# 签到动作
@login_required
def sign_index_action(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    phone = request.POST.get('phone', '')
    # 已签到数
    already_count = Guest.objects.filter(event_id=event_id).filter(sign=1).count()
    # 当前发布会嘉宾数
    total_count = Guest.objects.filter(event_id=event_id).count()


    result = Guest.objects.filter(phone = phone)
    if not request:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'phone error.',
                                                   'total_count': total_count,
                                                   'already_count': already_count})

    result = Guest.objects.filter(phone = phone, event_id = event_id)
    if not result:
        return render(request, 'sign_index.html',{'event': event,
                                                  'hint': 'event id or phone error.',
                                                  'total_count': total_count,
                                                  'already_count': already_count})

    result = Guest.objects.get(phone = phone)
    if result.sign:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': "user has sign in.",
                                                   'total_count': total_count,
                                                   'already_count': already_count})
    else:
        Guest.objects.filter(phone = phone).update(sign = '1')
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint':'sing in success!',
                                                   'guest': result,
                                                   'total_count': total_count,
                                                   'already_count': already_count})
