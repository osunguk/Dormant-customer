from django.shortcuts import render,redirect
from .models import Content, Profile
from django.contrib.auth.models import User, Group,AnonymousUser
from django.contrib import auth

from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Max
import datetime
from apscheduler.schedulers.background import BackgroundScheduler

#휴면계정 알림
def dormant_Alert():
    userList = User.objects.values()

    for users in userList:
        last_login = users['last_login']
        now = datetime.datetime.now(timezone.utc)
        if last_login is None:
            last_login = users['date_joined']
        if now == (last_login + datetime.timedelta(days=335)): # 휴면계정 변환 30일 전 알림
            print('ID : '+users['username'] + '은(는) 30일 뒤 휴면계정으로 전환됩니다.')
    #print('Background scheduler \'dormant_Alter()\' start')

#휴면계정 전환
def change_AccountGroup():
    userList = User.objects.values()
    dormant_group = Group.objects.get(name='dormant_account')
    general_group = Group.objects.get(name='General users')
    for users in userList:
        user = User.objects.get(username=users['username']) #유저리스트에서 username 가져옴
        last_login = users['last_login']

        now = datetime.datetime.now(timezone.utc)
        if last_login is None:
            last_login = users['date_joined']

        # 365일 이상 접속 X ==> 일반그룹 -> 휴면그룹으로 이동
        if (now - last_login).days >= 365:
            dormant_group.user_set.add(user)
            user.groups.remove(general_group)
            print('ID : '+users['username'] + '은(는) 휴면계정으로 전환되었습니다.')

            """
            tempgroup = User.groups.through.objects.get(user=users)
            tempgroup.group = dormant_group
            tempgroup.save()
            """

sched = BackgroundScheduler()
sched.add_job(change_AccountGroup, 'interval', seconds=60)
sched.add_job(dormant_Alert, 'interval', seconds=3)
sched.start()



def home(request):
    return render(request,'app/home.html')


def login(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        pwd = request.POST.get('pwd')
        user = auth.authenticate(request, username=name, password=pwd) #인증
        general_group = Group.objects.get(name='General users')
        check_DormantAccount = user.groups.filter(name='dormant_account').exists()
        content_all = Content.objects.all()
        total_content = len(content_all)  # 총 게시물 수
        if user is not None:
            auth.login(request, user)
            #Profile(dormant_count = 0).save()  # 로그인 했을 때 휴면 계정 전환 카운트 초기화
            if user.groups.filter(name='dormant_account').exists():  # 휴면계정일때 로그인 하면 일반그룹으로 이동
                tempgroup = User.groups.through.objects.get(user=user)  # 임시그룹
                tempgroup.group = general_group
                tempgroup.save()
            return render(request, 'app/board.html',{'check_DormantAccount':check_DormantAccount,'contents': content_all,'total':total_content})
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
        user = User.objects.create_user(username=username,password=userpwd)

        # 회원가입 후 일반유저 그룹에 추가
        general_group = Group.objects.get(name='General users')
        general_group.user_set.add(user)
        # auth.login(request,user)
        return redirect(to='home')

    return render(request, 'app/signup.html')


def write(request):
    number = Content.objects.aggregate(number=Max('number'))

    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST.get('content')
        Content.user = request.user
        Content(number=number.get('number')+1, title=title, contents=content, writer=User.get_username(Content.user)).save()
        return redirect(to='board')

    return render(request, 'app/write.html')


def board(request):
    content_all = Content.objects.all()
    total_content = len(content_all)# 총 게시물 수
    dormant_account = None
    user = request.user

    return render(request, 'app/board.html', {'contents': content_all,'dormant_account':dormant_account,'userdata':user,'total':total_content})


def user(request):
    user = request.user
    last_login = request.user.last_login
    joined_data = request.user.date_joined

    now = datetime.datetime.now(timezone.utc)
    day = (now - last_login).days
    result = (now - last_login)

    return render(request, 'app/user.html',{'name':user,'last_login':last_login,'joined_data':joined_data,'now':now,'result':result,'day':day})


def detail(request,number):  # 해당 number의 게시물을 불러와 html로 전송
    content = get_object_or_404(Content, number = number)

    return render(request,'app/detail.html',{'content':content})


def delete(request,number):
    content = Content.objects.get(number=number)
    if content.writer == request.user.get_username():  # 작성자와 사용자를 비교 일치시만 수정가능
        content.delete()
        return redirect('board')
    else:
        alert = True
        return render(request, 'app/detail.html', {'content': content, 'alert': alert})


def edit(request,number):
    content = Content.objects.get(number=number)
    if request.method == 'POST':  # 수정된 내용을 입력한후 detail로 이동
        content.title = request.POST['title']
        content.contents = request.POST['content']
        content.last_edit = datetime.datetime.now(timezone.utc)
        content.save()
        return render(request,'app/detail.html',{'content':content})
    else:  # 수정 페이지로 이동
        if content.writer == request.user.get_username():  # 작성자와 사용자를 비교 일치시만 수정가능
            return render(request,'app/edit.html',{'content':content})
        else:
            alert = True
            return render(request,'app/detail.html',{'content':content,'alert':alert})


def user_list(request):
    userList = User.objects.values()
    return render(request,'app/user_list.html',{'userList':userList})

