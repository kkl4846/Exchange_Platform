# from django.contrib.auth import login as auth_login
# from django.http import HttpResponse
import json
import jwt
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from . import models, forms, tokens, text
from config.my_settings import EMAIL
from django.contrib import auth
from django.views import View
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text


def user_main(request):
    ctx = {"user_main": user_main}
    return render(request, 'login/main.html', context=ctx)


def signup(request):
    if request.method == "POST":
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            new_user = models.User.objects.create_user(
                username=request.POST['username'], password=request.POST['password1'], nickname=request.POST['nickname'], email=request.POST['email'])
            auth.login(request, new_user)
            return redirect('login:user_main')
    else:
        form = forms.SignupForm()
    return render(request, 'login/signup.html', {'form': form})


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('login:user_main')
        else:
            return render(request, 'login/login.html', {'error': 'username or password is incorrect'})
    else:
        return render(request, 'login/login.html')


def mypage(request):
    context = {}
    if request.method == "POST":
        current_password = request.POST.get("origin_password")
        user = request.user
        if check_password(current_password, user.password):
            new_password = request.POST.get("password1")
            password_confirm = request.POST.get("password2")
            if new_password == password_confirm:
                user.set_password(new_password)
                user.save()
                auth.login(request, user)
                return redirect('login:mypage')
            else:
                context.update({'error': "새로운 비밀번호를 다시 확인해주세요."})
        else:
            context.update({'error': "현재 비밀번호가 일치하지 않습니다."})
    return render(request, 'login/mypage.html', context)


@csrf_exempt
def rename(request):
    req = json.loads(request.body)
    nickname = req['nickname']

    user = request.user
    user.nickname = nickname
    user.save()

    return JsonResponse({'nickname': nickname})


def certificate(request):
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

    if request.method == 'POST':
        user = request.user
        email = request.POST.get('email')

        if True:
            validate_email(email)

            current_site = get_current_site(request)
            domain = current_site.domain
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = tokens.school_certification_token.make_token(user)
            message_data = text.message(domain, uidb64, token)

            mail_title = "학교 인증을 완료해주세요"
            mail_to = email
            emailing = EmailMessage(mail_title, message_data, to=[mail_to])
            emailing.send()
            print('이메일 전송이 완료되었습니다.')
            return redirect('login:user_main')
        else:
            return redirect('login:certificate')

    else:
        ctx = {
            'school_names': school_names,
            'school_domains': school_domains,
            'school': school,
        }
        return render(request, 'login/certificate.html', context=ctx)


@csrf_exempt
def school_search(request):
    req = json.loads(request.body)
    school_name = req['school_name']

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
            user = models.User.objects.get(pk=uid)
            if user is not None and tokens.school_certification_token.check_token(user, token):
                user.school_certificate = 1
                user.save()
                return redirect(EMAIL['REDIRECT_PAGE'])
            return JsonResponse({"message": "AUTH FAIL"}, status=400)
        except ValidationError:
            return JsonResponse({"message": "TYPE_ERROR"}, status=400)
        except KeyError:
            return JsonResponse({"message": "INVALID_KEY"}, status=400)
