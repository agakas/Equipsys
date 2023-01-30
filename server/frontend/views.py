from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
import requests
from rest_framework.status import HTTP_400_BAD_REQUEST


# Create your views here.
#Рендер страницы входа или переход а главную страницу если есть авторизация
def sign_in(request):
    if request.user.is_authenticated:
        return redirect('/main')
    return render(request, 'frontend/signin.html')

def sign_in_action(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/main')
        else:
            messages.error(request, 'Неверный логин или пароль')
            return redirect('/')
    return render(request, 'frontend/signin.html')

def sign_up(request):
    return render(request, 'frontend/signup.html')

def sign_up_action(request):
    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')
        new_password = request.POST.get('password')

        post_data = dict(username = new_username, email = new_email, password = new_password)
        response = requests.post('http://127.0.0.1:8000/api/app/users/', data=post_data)

        if response.status_code == 400:
            messages.error(request, 'Логин уже существует')
            return redirect('/sign_up')
        return redirect('/')
    return render(request, 'frontend/signup.html')

#Выход из аккаунта
def log_out(request):
    log_out(request)
    return redirect('/')

#для главной страницы пользователя, в случае админа - страницы админа
def home(request):
    if request.user.is_superuser:
        return render(request, 'frontend/home-admin.html')  #несозданный шаблон
    return render(request, 'frontend/home-user.html')

#def sign_up(request):
#    if request.user.is_superuser:
#        pass
#    return render(request, 'frontend/home.html')