import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.views import View
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.db import IntegrityError
from django.core.paginator import Paginator
from . import tokens, text, helper
from .models import *
from domestic.models import *
from foreign.models import *
from country.models import *

URL_LOGIN = '/login/'


def user_main(request):
    ctx = {"user_main": user_main}
    return render(request, 'login/main.html', context=ctx)


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['real_password']
        if len(username) > 30:
            return render(request, 'login/signup.html', {'error': "아이디는 30자를 초과할 수 없습니다."})
        else:
            try:
                new_user = User.objects.create_user(
                    username=username, password=password, nickname=request.POST['nickname'], email=request.POST['email'])
                auth.login(request, new_user)
                return redirect('login:user_main')
            except IntegrityError as e:
                if repr(e) == "IntegrityError('UNIQUE constraint failed: login_user.username')":
                    return render(request, 'login/signup.html', {'error': "이미 사용 중인 아이디입니다."})
                elif repr(e) == "IntegrityError('UNIQUE constraint failed: login_user.nickname')":
                    return render(request, 'login/signup.html', {'error': "이미 사용 중인 닉네임입니다."})
                elif repr(e) == "IntegrityError('UNIQUE constraint failed: login_user.email')":
                    return render(request, 'login/signup.html', {'error': "이미 사용 중인 이메일입니다."})
    else:
        return render(request, 'login/signup.html')


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['real_password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('login:user_main')
        else:
            return render(request, 'login/login.html', {'login_error': True})
    else:
        return render(request, 'login/login.html')


@login_required(login_url=URL_LOGIN)
def mypage(request):
    context = {}
    if request.method == "POST":
        origin_password = request.POST.get("origin_password")
        user = request.user
        if check_password(origin_password, user.password):
            new_password = request.POST.get("real_password")
            user.set_password(new_password)
            user.save()
            auth.login(request, user)
            context.update({'message': "비밀번호 변경이 완료되었습니다."})
        else:
            context.update({'message': "기존 비밀번호를 확인해주세요."})
    return render(request, 'login/mypage.html', context)


@csrf_exempt
def rename(request):
    req = json.loads(request.body)
    nickname = req['nickname']

    user = request.user
    user.nickname = nickname
    user.save()

    return JsonResponse({'nickname': nickname})


@login_required(login_url=URL_LOGIN)
def certificate(request):
    f = open('config/univ.json', 'r')
    file = json.load(f)

    school_names = []
    for university_dicts in file:
        for university_name in (university_dicts.get(key) for key in university_dicts.keys() if 'ko-name' in key):
            school_names.append(university_name)
    school_names.sort()

    if request.method == 'POST':
        user = request.user
        email = request.POST.get('email')
        school_domain = request.POST.get('school_domain')
        try:
            user.email = email
            user.save()
        except IntegrityError:
            ctx = {
                'alert_flag': True,
                'school_names': school_names
            }
            return render(request, 'login/certificate.html', context=ctx)

        if email.endswith(school_domain) == True:
            validate_email(email)

            current_site = get_current_site(request)
            domain = current_site.domain
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = tokens.school_certification_token.make_token(user)
            message_data = text.message(domain, uidb64, token)

            mail_title = "Uni Connect: 학교 인증을 완료해주세요"
            mail_to = email
            emailing = EmailMessage(mail_title, message_data, to=[mail_to])
            emailing.send()
            return render(request, 'login/send_email.html')
        else:
            domain_error = "이메일 도메인이 일치하지 않습니다."
            ctx = {
                'domain_error': domain_error,
                'school_names': school_names,
            }
            return render(request, 'login/certificate.html', context=ctx)

    else:
        ctx = {
            'school_names': school_names,
        }
        return render(request, 'login/certificate.html', context=ctx)


@login_required(login_url=URL_LOGIN)
@csrf_exempt
def school_search(request):
    req = json.loads(request.body)
    school_name = req['school_name']

    user = request.user
    user.university = school_name
    user.save()

    f = open('config/univ.json', 'r')
    file = json.load(f)

    school_names = []
    school_domains = []
    for university_dicts in file:
        for university_name in (university_dicts.get(key) for key in university_dicts.keys() if 'ko-name' in key):
            school_names.append(university_name)
        for key in university_dicts.keys():
            if 'ko-name' in key:
                school_domains.append(university_dicts.get('domains')[0])

    school = dict(zip(school_names, school_domains))

    school_domain = school[school_name]
    return JsonResponse({'school_domain': school_domain})


class Activate(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            if user is not None and tokens.school_certification_token.check_token(user, token):
                user.school_certificate = 1
                user.save()
                return render(request, 'login/success_email.html')
            return JsonResponse({"message": "AUTH FAIL"}, status=400)
        except ValidationError:
            return JsonResponse({"message": "TYPE_ERROR"}, status=400)
        except KeyError:
            return JsonResponse({"message": "INVALID_KEY"}, status=400)


@login_required(login_url=URL_LOGIN)
def myquestion(request):
    user = request.user
    d_questions = DQuestion.objects.filter(author=user).order_by('-pk')
    paginator1 = Paginator(d_questions, 10)
    page_number1 = request.GET.get('page1')
    d_question_list = paginator1.get_page(page_number1)

    f_questions = FQuestion.objects.filter(author=user).order_by('-pk')
    paginator2 = Paginator(f_questions, 10)
    page_number2 = request.GET.get('page2')
    f_question_list = paginator2.get_page(page_number2)

    c_questions = CQuestion.objects.filter(author=user).order_by('-pk')
    paginator3 = Paginator(c_questions, 10)
    page_number3 = request.GET.get('page3')
    c_question_list = paginator3.get_page(page_number3)

    ctx = {
        'd_question_list': d_question_list,
        'f_question_list': f_question_list,
        'c_question_list': c_question_list,
    }
    return render(request, 'login/myquestion.html', context=ctx)


@login_required(login_url=URL_LOGIN)
def mycomment(request):
    user = request.user
    d_comments = DComment.objects.filter(comment_author=user).order_by('-pk')
    paginator1 = Paginator(d_comments, 10)
    page_number1 = request.GET.get('page1')
    d_comment_list = paginator1.get_page(page_number1)

    f_comments = FComment.objects.filter(comment_author=user).order_by('-pk')
    paginator2 = Paginator(f_comments, 10)
    page_number2 = request.GET.get('page2')
    f_comment_list = paginator2.get_page(page_number2)

    c_comments = CComment.objects.filter(comment_author=user).order_by('-pk')
    paginator3 = Paginator(c_comments, 10)
    page_number3 = request.GET.get('page3')
    c_comment_list = paginator3.get_page(page_number3)

    ctx = {
        'd_comment_list': d_comment_list,
        'f_comment_list': f_comment_list,
        'c_comment_list': c_comment_list,
    }
    return render(request, 'login/mycomment.html', context=ctx)


def reset_password(request):
    ctx = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        try:
            target_user = User.objects.get(
                username=username, email=email)
            auth_num = helper.email_auth_num()
            target_user.set_password(auth_num)
            target_user.save()
            message_data = text.password_message(auth_num)

            mail_title = "Uni Connect: 임시 비밀번호입니다."
            mail_to = email
            emailing = EmailMessage(mail_title, message_data, to=[mail_to])
            emailing.send()
            return render(request, 'login/email_for_password.html')
        except:
            reset_error = "회원 정보를 다시 확인해주세요."
            ctx.update({'reset_error': reset_error})

    return render(request, 'login/reset_password.html', context=ctx)
