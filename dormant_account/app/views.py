from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from django.utils import timezone
from django.core.mail import EmailMessage
from django.db.models import Max

import datetime

from .models import Content, Profile, DormantUserInfo, UserB, UserC
from apscheduler.schedulers.background import BackgroundScheduler


# 휴면계정 알림
def dormant_Alert():
    user_list = User.objects.values()
    for users in user_list:
        u = User.objects.get(id=users['id'])

        last_login = users['last_login']
        if last_login is None:
            last_login = users['date_joined']
        dormant_Time = datetime.timedelta(days=365) + last_login - timezone.now()  # 계정 전환 남은기간 계산
        Profile.objects.filter(user_id=users['id']).update(dormant_cnt=dormant_Time.days)
        if dormant_Time.days <= 90:  # 휴면계정 변환 90일 전에만 하루알림 if dormant_Time.days == 90:
            if Profile.objects.get(user=u).email:
                if not Profile.objects.get(user=u).check_alert:
                    email = EmailMessage('ZEROGO 휴면 전환 알림',
                                         """
                    안녕하세요. 제로고입니다.
    회원님의 개인정보보호를 위해 1년 이상 사람인 서비스를 이용하지 않은 계정에 한해 정보통신망 이용 촉진 및 정보보호 등에 관한 법률에 따라 휴면 계정으로 전환될 예정입니다.
    회원님은 {} 까지 제로고 서비스 이용이 없을 경우 휴면 계정으로 전환될 예정이오니, 이를 원치 않으실 경우 로그인을 해주시기 바랍니다.
    또한, 휴면계정으로 전환되어도 아이디/비밀번호로 로그인 하면 해제할 수 있으나, 아래와 같은 서비스에 대한 변경사항이 있으니 참고 바랍니다.
    
    휴면 계정 전환 시 변경 사항
    - 회원의 개인정보는 별도 분리하여 보관
    - 메일 발송 중지
    """.format(last_login + datetime.timedelta(days=365)), to=[Profile.objects.get(user=u).email])
                    email.send()
                    Profile.objects.filter(user=u).update(check_alert=True)
                    memo = Profile.objects.get(user=u).memo + '\n' + str(timezone.now()) + ' 시간부로 사전 알림 메세지 전송'
                    Profile.objects.filter(user=u).update(memo=memo)
                else:
                    pass
        if dormant_Time.days <= 60:  # 계정 전환 60일 전 필터 값 update
            Profile.objects.filter(user_id=users['id']).update(dormantNotice_day_filter=True)


# 휴면계정 전환
def change_AccountGroup():
    user_list = User.objects.values()
    for users in user_list:
        user = User.objects.get(id=users['id'])  # 유저리스트에서 username 가져옴
        last_login = users['last_login']

        now = datetime.datetime.now(timezone.utc)
        if last_login is None:
            last_login = users['date_joined']

        # 365일 이상 접속 X ==> 일반그룹 -> 휴면그룹으로 이동
        if (now - last_login).days >= 365:
            U = User.objects.get(username=user)  # 일반계정의 데이터를 휴면계정으로 옮김
            dormant = DormantUserInfo()  # 생성할 휴면계정
            dormant.id = U.id
            dormant.lastLogin = last_login
            dormant.dormantDate = last_login + datetime.timedelta(days=365)
            dormant.memo = Profile.objects.get(user=U).memo + '\n' + str(timezone.now())+' 시간부로 휴면계정으로 전환'
            if Profile.objects.get(user=U).role_profile == 1:
                dormant.deleteDate = dormant.dormantDate + datetime.timedelta(days=1780)
            else:
                dormant.deleteDate = dormant.dormantDate + datetime.timedelta(days=365)
            dormant.username = U.username
            dormant.email = Profile.objects.get(user=U).email
            dormant.phoneNumber = Profile.objects.get(user=U).phoneNumber
            dormant.role_dormant = Profile.objects.get(user=U).role_profile
            if dormant.role_dormant == 1:  # 비즈니스
                 ub = UserB.objects.get(user_b=U)
                 dormant.company_name = ub.company_name
                 dormant.business_number = ub.business_number
                 dormant.star_point = ub.star_point
            elif dormant.role_dormant == 2:  # 커스텀
                uc = UserC.objects.get(user_c=U)
                dormant.kakao_Id = uc.kakao_Id
                dormant.mining_point = uc.mining_point
            else:
                pass
            dormant.save()
            U.delete()
            # print('ID : ' + users['username'] + '은(는) 휴면계정으로 전환되었습니다.')


def dormant_process():
    user_list = DormantUserInfo.objects.values()
    for user in user_list:
        if user['deleteDate'] - timezone.now() < datetime.timedelta(days=0):
            d = DormantUserInfo.objects.get(username=user['username'])
            print(d.username+' : 삭제')
            # d.delete()


sched = BackgroundScheduler()
sched.add_job(change_AccountGroup, 'interval', seconds=3)
sched.add_job(dormant_Alert, 'interval', seconds=5)
sched.add_job(dormant_process, 'interval', seconds=3)
sched.start()


def home(request):
    return render(request, 'app/home.html')


def login(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        pwd = request.POST.get('pwd')
        user = auth.authenticate(request, username=name, password=pwd)  # 인증

        content_all = Content.objects.all()
        total_content = len(content_all)  # 총 게시물 수
        check_DormantAccount = DormantUserInfo.objects.filter(username=name).exists() # 휴면계정 확인

        if check_DormantAccount: # 휴면계정 삭제 & 일반 계정 생성
            d = DormantUserInfo.objects.get(username=name)
            User.objects.create_user(username=d.username, password=pwd, last_login=timezone.now())
            u = Profile.objects.get(user=User.objects.get(username=name))
            u.email = d.email
            u.phoneNumber = d.phoneNumber
            u.role_profile = d.role_dormant
            u.memo = d.memo + '\n' + str(timezone.now()) + ' 시간부로 일반계정으로 전환'
            if d.role_dormant == 1:
                b = UserB()
                b.user_b = User.objects.get(username=name)
                b.company_name = d.company_name
                b.business_number = d.business_number
                b.star_point = d.star_point
                b.save()
            elif d.role_dormant == 2:
                c = UserC()
                c.user_c = User.objects.get(username=name)
                c.kakao_Id = d.kakao_Id
                c.mining_point = d.mining_point
                c.save()
            else:
                pass  # 타입이 없는 사용자
            u.save()
            user = auth.authenticate(request, username=name, password=pwd)
            d.delete()

        if user is not None:
            auth.login(request, user)
            Profile.objects.filter(user_id=user.id).update(check='')
            User.objects.filter(username=name).update(last_login=timezone.now())  # 마지막 로그인 시간 최신화
            return render(request, 'app/board.html',
                          {'contents': content_all,
                           'total': total_content,'check_DormantAccount':check_DormantAccount})
        else:
            return render(request, 'app/login.html', {'error': '잘못된 id 또는 pwd 입니다'})
    else:
        return render(request, 'app/login.html')


def logout(request):
    auth.logout(request)
    return redirect(to='home')


def signup(request):
    if request.method == 'POST':
        username = request.POST['name']
        email = request.POST['email']
        phoneNumber = request.POST['phoneNumber']
        check_id = User.objects.filter(username=username).exists()
        if check_id:  # id가 중복일때 signup 거부
            pass
        userpwd = request.POST['pwd']
        user = User.objects.create_user(username=username, password=userpwd, last_login=timezone.now())
        Profile.objects.filter(user_id=user).update(email=email)
        Profile.objects.filter(user_id=user).update(phoneNumber=phoneNumber)
        if request.POST.get('type') == 'Business':
            Profile.objects.filter(user=user).update(role_profile=1)
            return render(request,'app/business.html',{'username':user.username})
        else:
            Profile.objects.filter(user=user).update(role_profile=2)
            return render(request, 'app/customer.html',{'username':user.username})
    return render(request, 'app/signup.html')


def write(request):
    number = Content.objects.aggregate(number=Max('number'))
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST.get('content')
        Content.user = request.user
        if number.get('number') is None:
            Content(number=1, title=title,
                    contents=content, writer=User.get_username(Content.user)).save()
        else:
            Content(number=number.get('number') + 1, title=title,
                    contents=content, writer=User.get_username(Content.user)).save()
        return redirect(to='board')
    return render(request, 'app/write.html')


def board(request):
    content_all = Content.objects.all()
    total_content = len(content_all)  # 총 게시물 수
    dormant_account = None
    user = request.user
    return render(request, 'app/board.html',
                  {'contents': content_all, 'dormant_account': dormant_account, 'userdata': user,
                   'total': total_content})


def user(request):
    user = request.user
    last_login = request.user.last_login
    joined_data = request.user.date_joined
    now = datetime.datetime.now(timezone.utc)
    day = (now - last_login).days
    result = (now - last_login)
    return render(request, 'app/user.html',{'name': user, 'last_login': last_login, 'joined_data': joined_data, 'now': now, 'result': result,'day': day})


def detail(request, number):  # 해당 number의 게시물을 불러와 html로 전송
    content = get_object_or_404(Content, number=number)
    return render(request, 'app/detail.html', {'content': content})


def delete(request, number):
    content = Content.objects.get(number=number)
    if content.writer == request.user.get_username():  # 작성자와 사용자를 비교 일치시만 수정가능
        content.delete()
        return redirect('board')
    else:
        alert = True
        return render(request, 'app/detail.html', {'content': content, 'alert': alert})


def edit(request, number):
    content = Content.objects.get(number=number)
    if request.method == 'POST':  # 수정된 내용을 입력한후 detail로 이동
        content.title = request.POST['title']
        content.contents = request.POST['content']
        content.last_edit = datetime.datetime.now(timezone.utc)
        content.save()
        return render(request, 'app/detail.html', {'content': content})
    else:  # 수정 페이지로 이동
        if content.writer == request.user.get_username():  # 작성자와 사용자를 비교 일치시만 수정가능
            return render(request, 'app/edit.html', {'content': content})
        else:
            alert = True
            return render(request, 'app/detail.html', {'content': content, 'alert': alert})


def user_list(request):
    pList = Profile.objects.values()
    result = []
    for x in list(pList):
        u = User.objects.get(id=x['user_id'])
        sentence = u.username + '의 휴면계정 전환까지 남은 기간 : ' + str(x['dormant_cnt']) + '일'
        if x['dormant_cnt'] < 0:
            sentence = u.username + '는 휴면계정입니다'
        result.append(sentence)
    return render(request, 'app/user_list.html', {'results':result})


def customer(request):
    if request.method == 'POST':
        kakao_id = request.POST['kakao_id']
        username = request.POST.get('username')
        user = User.objects.get(username=username)
        u = UserC()
        u.kakao_Id = kakao_id
        u.mining_point = 0
        u.user_c = user
        u.save()
        return render(request, 'app/home.html', {'kakao_id' : kakao_id})
    return render(request, 'app/customer.html')


def business(request):
    if request.method == 'POST':
        business_num = request.POST['business_num']
        company_name = request.POST['company_name']
        username = request.POST.get('username')
        user = User.objects.get(username=username)
        u = UserB()
        u.business_number = business_num
        u.company_name = company_name
        u.star_point = 0
        u.user_b = user
        u.save()
        return render(request, 'app/home.html', {'business_num' : business_num})
    return render(request, 'app/business.html')