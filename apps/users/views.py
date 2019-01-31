from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.shortcuts import render
from django.views import View

from users.forms import LoginForm, RegisterForm
from users.models import UserProfile, EmailVerifyRecord
from utils.email_send import send_register_email


class CustomBackend(ModelBackend):
    """
    重写的验证登录
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):  # 明文密码传进去加密对比user的密码
                return user
        except Exception as e:
            return None

        # return super().authenticate(request, username, password, **kwargs)


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request,'active_fail.html')
        return render(request, 'login.html')



class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():  # 检查error是否为空
            username = request.POST.get('email', '')
            if UserProfile.objects.filter(email=username):
                return render(request, 'register.html', {'register_form': register_form,
                                                         'msg': '用户已经存在'})
            password = request.POST.get('password', '')
            user_profile = UserProfile(username=username, email=username, is_active=False,
                                       password=make_password(password))
            user_profile.save()

            send_register_email(username, 'register')
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form': register_form})


class LoginView(View):
    """
    采用类的方式
    """

    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():  # 检查error是否为空
            username = request.POST.get('email', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)  # settings设置后并不用改代码就能直接调用自定义auth
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {'msg': '用户名未激活！'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误！'})
        else:
            return render(request, 'login.html', {'login_form': login_form})

# Create your views here.
# def user_login(request):
#     """
#     平台统一登录
#     :param request:
#     :return:
#     """
#     if request.method == 'POST':
#         username = request.POST.get('username','')
#         password = request.POST.get('password','')
#         user = authenticate(username=username,password=password)
#         if user is not None:
#             login(request,user)
#             return render(request, 'index.html')
#         else:
#             return render(request, 'login.html',{'msg':'用户名或密码错误！'})
#     elif request.method == 'GET':
#         return render(request, 'login.html')

class ForgetPwdView(View):
    def get(self, request):
        return render(request, 'forgetpwd.html')
