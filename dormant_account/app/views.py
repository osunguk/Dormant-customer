import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.mail import EmailMessage
from django.db.models import Max
from django.shortcuts import (
    render, redirect, get_object_or_404,
)
from django.utils import timezone

from .models import (
    Content, Profile, DormantUserInfo,
    UserB, UserC,
)


def dormant_alert():  # 휴면계정 알림
    _user_list = User.objects.values()
    mail_message_file = open('app/mail_message', 'rt', encoding='UTF-8')

    for users in _user_list:
        u = User.objects.get(id=users['id'])
        last_login = users['last_login']
        _dormant_time = last_login + datetime.timedelta(days=365)
        if last_login is None:
            last_login = users['date_joined']
        dormant_time = datetime.timedelta(days=365) + last_login - timezone.localtime()  # 계정 전환 남은기간 계산
        Profile.objects.filter(user_id=users['id']).update(dormant_cnt=dormant_time.days)
        if dormant_time.days <= 90:  # 휴면계정 변환 90일 전에만 하루알림 if dormant_Time.days == 90:
            if Profile.objects.get(user=u).email:
                if not Profile.objects.get(user=u).check_alert:
                    email_message = EmailMessage('ZEROGO 휴면 전환 알림',
                                                 mail_message_file.read().format(_dormant_time.strftime('%Y-%m-%d %H:%M')),
                                                 to=[Profile.objects.get(user=u).email])
                    email_message.send()
                    Profile.objects.filter(user=u).update(
                        check_alert=True,
                        memo=Profile.objects.get(user=u).memo + '\n' + str(timezone.localtime()) + ' 시간부로 사전 알림 메세지 전송')
                else:
                    pass
        if dormant_time.days <= 60:  # 계정 전환 60일 전 필터 값 update
            Profile.objects.filter(user_id=users['id']).update(conversion_check=True)


def change_account_group():  # 휴면계정 전환
    _user_list = User.objects.values()
    for users in _user_list:
        U = User.objects.get(id=users['id'])  # 유저리스트에서 username 가져옴
        last_login = users['last_login']
        if last_login is None:
            last_login = users['date_joined']

        # 365일 이상 접속 X ==> 일반그룹 -> 휴면그룹으로 이동
        if (timezone.localtime() - last_login).days >= 365:
            dormant = DormantUserInfo(  # 생성할 휴면계정
                id=U.id,
                last_login=last_login,
                dormant_date=last_login + datetime.timedelta(days=365),
                memo=Profile.objects.get(user=U).memo + '\n' + str(timezone.localtime()) + ' 시간부로 휴면계정으로 전환',
                username=U.username,
                email=Profile.objects.get(user=U).email,
                phone_number=Profile.objects.get(user=U).phone_number,
                role_dormant=Profile.objects.get(user=U).role_profile
            )
            if Profile.objects.get(user=U).role_profile == 1:
                dormant.delete_date = dormant.dormant_date + datetime.timedelta(days=1780)
                ub = UserB.objects.get(user_b=U)
                dormant.company_name = ub.company_name
                dormant.business_number = ub.business_number
                dormant.star_point = ub.star_point
            elif dormant.role_dormant == 2:  # 커스텀
                dormant.delete_date = dormant.dormant_date + datetime.timedelta(days=365)
                uc = UserC.objects.get(user_c=U)
                dormant.kakao_id = uc.kakao_id
                dormant.mining_point = uc.mining_point
            else:
                pass
            dormant.save()
            U.delete()


def dormant_process():
    _user_list = DormantUserInfo.objects.values()
    for _user in _user_list:
        if _user['delete_date'] - timezone.localtime() < datetime.timedelta(days=0):
            d = DormantUserInfo.objects.get(username=_user['username'])
            print(d.username + ' : 삭제')
            # d.delete()


schedule = BackgroundScheduler()
schedule.add_job(change_account_group, 'interval', seconds=3)
schedule.add_job(dormant_alert, 'interval', seconds=5)
schedule.add_job(dormant_process, 'interval', seconds=3)
schedule.start()


def home(request):
    return render(request, 'app/home.html')


def login(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        pwd = request.POST.get('pwd')
        _user = auth.authenticate(request, username=name, password=pwd)  # 인증

        check_dormant_account = DormantUserInfo.objects.filter(username=name).exists()  # 휴면계정 확인

        if check_dormant_account:  # 휴면계정 삭제 & 일반 계정 생성
            d = DormantUserInfo.objects.get(username=name)
            User.objects.create_user(username=d.username, password=pwd, last_login=timezone.localtime())
            Profile.objects.filter(user=User.objects.get(username=name)).update(
                email=d.email,
                phone_number=d.phone_number,
                role_profile=d.role_dormant,
                memo=d.memo + '\n' + str(timezone.localtime()) + ' 시간부로 일반계정으로 전환'
            )
            if d.role_dormant == 1:
                UserB(
                    user_b=User.objects.get(username=name),
                    company_name=d.company_name,
                    business_number=d.business_number,
                    star_point=d.star_point
                ).save()
            elif d.role_dormant == 2:
                UserC(
                    user_c=User.objects.get(username=name),
                    kakao_id=d.kakao_id,
                    mining_point=d.mining_point
                ).save()
            else:
                pass  # 타입이 없는 사용자
            _user = auth.authenticate(request, username=name, password=pwd)
            d.delete()

        if _user is not None:
            auth.login(request, _user)
            User.objects.filter(username=name).update(last_login=timezone.localtime())  # 마지막 로그인 시간 최신화
            return render(request, 'app/board.html', {'contents': Content.objects.all(),
                                                      'total': len(Content.objects.all()),
                                                      'check_dormant_account': check_dormant_account})
        else:
            return render(request, 'app/login.html', {'error': '잘못된 id 또는 pwd 입니다'})
    else:
        return render(request, 'app/login.html')


def logout(request):
    auth.logout(request)
    return redirect(to='home')


def signup(request):
    if request.method == 'POST':
        if User.objects.filter(username=request.POST['name']).exists():  # id가 중복일때 signup 거부
            pass
        _user = User.objects.create_user(
            username=request.POST['name'],
            password=request.POST['pwd'],
            last_login=timezone.localtime()
        )
        Profile.objects.filter(user_id=_user).update(
            email=request.POST['email'],
            phone_number=request.POST['phone_number']
        )
        if request.POST.get('type') == 'Business':
            Profile.objects.filter(user=_user).update(role_profile=1)
            return render(request, 'app/business.html', {'username': _user.username})
        else:
            Profile.objects.filter(user=_user).update(role_profile=2)
            return render(request, 'app/customer.html', {'username': _user.username})
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
    _user = request.user
    return render(request, 'app/board.html',
                  {'contents': content_all, 'dormant_account': dormant_account,
                   'userdata': _user, 'total': total_content})


def user(request):
    return render(request, 'app/user.html', {'name': request.user, 'last_login': request.user.last_login,
                                             'joined_data': request.user.date_joined, 'now': timezone.localtime(),
                                             'result': timezone.localtime() - request.user.last_login,
                                             'day': (timezone.localtime() - request.user.last_login).days})


def detail(request, number):  # 해당 number의 게시물을 불러와 html로 전송
    return render(request, 'app/detail.html', {'content': get_object_or_404(Content, number=number)})


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
        content.last_edit = timezone.localtime()
        content.save()
        return render(request, 'app/detail.html', {'content': content})
    else:  # 수정 페이지로 이동
        if content.writer == request.user.get_username():  # 작성자와 사용자를 비교 일치시만 수정가능
            return render(request, 'app/edit.html', {'content': content})
        else:
            alert = True
            return render(request, 'app/detail.html', {'content': content, 'alert': alert})


def user_list(request):
    result = []
    for x in list(Profile.objects.values()):
        u = User.objects.get(id=x['user_id'])
        sentence = u.username + '의 휴면계정 전환까지 남은 기간 : ' + str(x['dormant_cnt']) + '일'
        if x['dormant_cnt'] < 0:
            sentence = u.username + '는 휴면계정입니다'
        result.append(sentence)
    return render(request, 'app/user_list.html', {'results': result})


def customer(request):
    if request.method == 'POST':
        UserC(kakao_id=request.POST['kakao_id'],
              mining_point=0,
              user_c=User.objects.get(username=request.POST.get('username')))
        return render(request, 'app/home.html')
    return render(request, 'app/customer.html')


def business(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        UserB(business_number=request.POST['business_num'],
              company_name=request.POST['company_name'],
              star_point=0,
              user_b=User.objects.get(username=username))
        return render(request, 'app/home.html')
    return render(request, 'app/business.html')
