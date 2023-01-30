from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages

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
    return True #надо отправить на регистрацию и проверить ошибку

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