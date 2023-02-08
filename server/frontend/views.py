import json
from django.contrib.auth import authenticate, login, logout, _get_user_session_key
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
import requests
from django.template.context_processors import csrf
from django.utils.safestring import SafeString


# Create your views here.
def sign_in(request):
    if request.user.is_authenticated:
        return redirect('/main')
    return render(request, 'frontend/signin.html')

def sign_in_action(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        response = requests.post('http://127.0.0.1:8000/api/app/login_user/', {'username': username, 'password': password})
        if response.status_code == 200:
            resp = redirect('/main')
            response_cookies = response.cookies
            current_cookies = dict(response_cookies)
            resp.set_cookie('csrftoken', current_cookies['csrftoken'])
            resp.set_cookie('sessionid', current_cookies['sessionid'])
            print('Посылаемые сервером в браузер куки:')
            print(current_cookies)
            return resp
            #return redirect('/main')
        messages.error(request, 'Неверный логин или пароль')
        return redirect('/')

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
    #logout(request)
    cookies_now = {'csrftoken': request.COOKIES.get('csrftoken'), 'sessionid': request.COOKIES.get('sessionid')}
    response = requests.get('http://127.0.0.1:8000/api/app/logout_user/', cookies=cookies_now)
    return redirect('/')

#для главной страницы пользователя, в случае админа - страницы админа
def home(request):
    if request.user.is_authenticated:
        cookies_now = {'csrftoken': request.COOKIES.get('csrftoken'), 'sessionid': request.COOKIES.get('sessionid')}

        #Информация текущего аккаунта
        my_data = (requests.get("http://127.0.0.1:8000/api/app/current_user/", cookies=cookies_now)).json()
        current_data = {'my_data': my_data}

        if request.user.is_superuser:
            users_data = (requests.get("http://127.0.0.1:8000/api/app/users/", cookies=cookies_now)).json()
            organizations_data = (requests.get("http://127.0.0.1:8000/api/app/organizations/", cookies=cookies_now)).json()
            return render(request, 'frontend/home-admin.html', context=current_data)

        #информация об организациях пользователя
        current_organizations_data = (requests.get("http://127.0.0.1:8000/api/app/current_organizations/", cookies=cookies_now)).json()
        current_data['current_organizations'] = current_organizations_data
        #получаем оборудование для всех организаций текущего пользователя
        for org in current_data['current_organizations']:
            current_organizations_equipment = (requests.get("http://127.0.0.1:8000/api/app/equip_of_org/?org_id="+str(org['id']), cookies=cookies_now)).json()
            org['equipments'] = current_organizations_equipment
        # print('Гдееее тыыы')
        # print(my_data)
        # print('Гдееееееееее тыыыыыыыыыыы')
        return render(request, 'frontend/home-user.html', context=current_data)
        #return HttpResponse(my_data, content_type='application/json')
            #return render(request, 'frontend/home-admin.html', json.dumps(my_data))  #несозданный шаблон
        #return render(request, 'frontend/home-user.html')
    else:
        return redirect('/')


def delete_current_user(request):
    cookies_now = {'csrftoken': request.COOKIES.get('csrftoken'), 'sessionid': request.COOKIES.get('sessionid')}
    get_current_user = (requests.get("http://127.0.0.1:8000/api/app/current_user/", cookies=cookies_now)).json()
    id_current_user = get_current_user['id']
    headers = {}
    headers['X-CSRFToken'] = cookies_now['csrftoken']
    response = requests.delete("http://127.0.0.1:8000/api/app/users/"+str(id_current_user), cookies=cookies_now, headers=headers)
    print(response.status_code, response.content)
    return redirect('/')

def del_equip(request, equip_id):
    cookies_now = {'csrftoken': request.COOKIES.get('csrftoken'), 'sessionid': request.COOKIES.get('sessionid')}
    id_current_equipment = equip_id
    headers = {}
    headers['X-CSRFToken'] = cookies_now['csrftoken']
    response = requests.delete("http://127.0.0.1:8000/api/app/equipments/" + str(id_current_equipment), cookies=cookies_now, headers=headers)
    return redirect('/main')

def add_equip_of_org(request, org_id):
    cookies_now = {'csrftoken': request.COOKIES.get('csrftoken'), 'sessionid': request.COOKIES.get('sessionid')}
    headers = {}
    headers['X-CSRFToken'] = cookies_now['csrftoken']
    body = request.POST

    post_data = dict(serial = body['serial'], organization = org_id)
    response = requests.post("http://127.0.0.1:8000/api/app/equipments/", cookies=cookies_now, headers=headers, data=post_data)
    return redirect('/main')