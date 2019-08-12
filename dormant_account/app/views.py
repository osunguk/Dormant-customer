from django.shortcuts import render,redirect
from .models import Content
from django.contrib.auth.models import User
from django.contrib import auth

from django.utils import timezone
from django.shortcuts import get_object_or_404

import re
import datetime
# Create your views here.


def home(request):
    return render(request,'app/home.html')


def login(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        pwd = request.POST.get('pwd')
        user = auth.authenticate(request, username=name, password=pwd)
        if user is not None:
            auth.login(request, user)
            return redirect('board')
        else:
            return render(request, 'app/login.html',{'error':'잘못된 id 또는 pwd 입니다'})
    else:
        return render(request,'app/login.html')


def logout(request):
    auth.logout(request)
    return redirect(to='home')


def signup(request):
    if request.method == 'POST':
        username = request.POST['name']
        userpwd = request.POST['pwd']
        User.objects.create_user(username=username,password=userpwd)
        # auth.login(request,user)
        return redirect(to='home')

    return render(request, 'app/signup.html')


def write(request):
    cnt = len(Content.objects.all())
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST.get('content')
        Content.user = request.user
        Content(number=cnt + 1, title=title, contents=content, writer=User.get_username(Content.user)).save()
        return redirect(to='board')

    return render(request, 'app/write.html')


def board(request):
    content_all = Content.objects.all()
    dormant_account = None
    user = request.user

    return render(request, 'app/board.html', {'contents': content_all,'dormant_account':dormant_account,'userdata':user})


def user(request):
    user = request.user
    last_login = request.user.last_login
    joined_data = request.user.date_joined
    # num = re.findall("\d+", last_login)

    now = datetime.datetime.now(timezone.utc)

    result = (now - last_login)

    '''
    휴면계정 전환 30일전 통보
    if last_login + timedelta(days=335)
    
    '''

    return render(request, 'app/user.html',{'name':user,'last_login':last_login,'joined_data':joined_data,'now':now,'result':result})


def detail(request,number):  # 해당 number의 게시물을 불러와 html로 전송
    content = get_object_or_404(Content, number = number)

    return render(request,'app/detail.html',{'content':content})


def delete(request,number):
    return render(request,'/')


def edit(request,number):
    content = Content.objects.get(number=number)
    if request.method == 'POST':  # 수정된 내용을 입력한후 detail로 이동
        content.title = request.POST['title']
        content.contents = request.POST['content']
        content.last_edit = datetime.datetime.now(timezone.utc)
        content.save()
        return render(request,'app/detail.html',{'content':content})
        # return rediect(to='detail'+str(number))
    else:  # 수정 페이지로 이동
        if content.writer == request.user.get_username():  # 작성자와 사용자를 비교 일치시만 수정가능
            return render(request,'app/edit.html',{'content':content})
        else:
            alert = True
            return render(request,'app/detail.html',{'content':content,'alert':alert})


