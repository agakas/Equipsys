from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
import requests
from rest_framework import status
from rest_framework.permissions import IsAdminUser


# Create your views here.
def sign_in(request):
    if request.user.is_authenticated:
        return redirect('/main')
    return render(request, 'frontend/signin.html')

def sign_in_action(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        response = requests.post('http://127.0.0.1:8000/api/app/login_user/',
                                 {'username': username, 'password': password})
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
            organizations_data = (requests.get("http://127.0.0.1:8000/api/app/organizations/",
                                               cookies=cookies_now)).json()
            current_data['all_users'] = users_data
            current_data['all_orgs'] = organizations_data
            return render(request, 'frontend/home-admin.html', context=current_data)

        #информация об организациях пользователя
        current_organizations_data = (requests.get("http://127.0.0.1:8000/api/app/current_organizations/",
                                                   cookies=cookies_now)).json()
        current_data['current_organizations'] = current_organizations_data
        #получаем оборудование для всех организаций текущего пользователя
        for org in current_data['current_organizations']:
            current_organizations_equipment = (requests.get("http://127.0.0.1:8000/api/app/equip_of_org/?org_id="+str(org['id']),
                                                            cookies=cookies_now)).json()
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

#Вьюшки-обработчики экрана обычного пользователя
def delete_current_user(request):
    cookies_now = {'csrftoken': request.COOKIES.get('csrftoken'), 'sessionid': request.COOKIES.get('sessionid')}
    get_current_user = (requests.get("http://127.0.0.1:8000/api/app/current_user/", cookies=cookies_now)).json()
    id_current_user = get_current_user['id']
    headers = {}
    headers['X-CSRFToken'] = cookies_now['csrftoken']
    response = requests.delete("http://127.0.0.1:8000/api/app/users/"+str(id_current_user),
                               cookies=cookies_now, headers=headers)
    print(response.status_code, response.content)
    return redirect('/')

def delete_user_id(request, user_id):
    permission_classes = [IsAdminUser]
    cookies_now = {'csrftoken': request.COOKIES.get('csrftoken'), 'sessionid': request.COOKIES.get('sessionid')}
    headers = {}
    headers['X-CSRFToken'] = cookies_now['csrftoken']
    response = requests.delete("http://127.0.0.1:8000/api/app/users/"+str(user_id), cookies=cookies_now,
                               headers=headers)
    print(response.status_code, response.content)
    return redirect('/')

def del_equip(request, equip_id):
    cookies_now = {'csrftoken': request.COOKIES.get('csrftoken'), 'sessionid': request.COOKIES.get('sessionid')}
    id_current_equipment = equip_id
    headers = {}
    headers['X-CSRFToken'] = cookies_now['csrftoken']
    response = requests.delete("http://127.0.0.1:8000/api/app/equipments/" + str(id_current_equipment),
                               cookies=cookies_now, headers=headers)
    return redirect('/main')

def add_equip_of_org(request, org_id):
    cookies_now = {'csrftoken': request.COOKIES.get('csrftoken'), 'sessionid': request.COOKIES.get('sessionid')}
    print(cookies_now)
    headers = {}
    headers['X-CSRFToken'] = cookies_now['csrftoken']
    body = request.POST
    post_data = dict(serial = body['serial'], organization = org_id)
    print('Запрос add_equip_of_org')
    print(post_data)
    response = requests.post("http://127.0.0.1:8000/api/app/equipments/", cookies=cookies_now,
                             headers=headers, data=post_data)
    if response.status_code == 400:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    return HttpResponse(status=status.HTTP_200_OK)
    #return redirect('/main')

def edit_equip(request, equip_id):
    cookies_now = {'csrftoken': request.COOKIES.get('csrftoken'), 'sessionid': request.COOKIES.get('sessionid')}
    print(cookies_now)
    headers = {}
    headers['X-CSRFToken'] = cookies_now['csrftoken']
    body = request.POST
    patch_data = dict(serial=body['serial'])
    response = requests.patch("http://127.0.0.1:8000/api/app/equipments/" + str(equip_id) + "/", cookies=cookies_now,
                              headers=headers, data=patch_data)
    print("Ты заходи если шо")
    print(response.content)
    if response.status_code == 400:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    return HttpResponse(status=status.HTTP_200_OK)
def edit_current_user(request):
    cookies_now = {'csrftoken': request.COOKIES.get('csrftoken'), 'sessionid': request.COOKIES.get('sessionid')}
    headers = {}
    headers['X-CSRFToken'] = cookies_now['csrftoken']
    body = request.POST
    post_data = dict(username=body['username'], password=body['password'], email=body['email'])
    print("Это оно самое")
    print(post_data)
    print("А теперь пользователь")
    current_user = (requests.get("http://127.0.0.1:8000/api/app/current_user/", cookies=cookies_now)).json()
    response = requests.put("http://127.0.0.1:8000/api/app/users/"+str(current_user['id'])+"/", cookies=cookies_now,
                            headers=headers, data=post_data)
    if response.status_code == 400:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    return HttpResponse(status=status.HTTP_200_OK)


def user_to_admin(request, user_id):
    permission_classes = [IsAdminUser]
    cookies_now = {'csrftoken': request.COOKIES.get('csrftoken'), 'sessionid': request.COOKIES.get('sessionid')}
    headers = {}
    headers['X-CSRFToken'] = cookies_now['csrftoken']
    patch_data = dict(is_superuser = True)
    current_user = (requests.get("http://127.0.0.1:8000/api/app/current_user/", cookies=cookies_now)).json()
    response = requests.patch("http://127.0.0.1:8000/api/app/users/" + str(user_id)+"/", cookies=cookies_now,
                              headers=headers, data=patch_data)
    response_cookies = response.cookies
    current_cookies = dict(response_cookies)
    resp = redirect('/main')
    resp.set_cookie('sessionid', current_cookies['sessionid'])
    return resp

def delete_org(request, org_id):
    permission_classes = [IsAdminUser]
    cookies_now = {'csrftoken': request.COOKIES.get('csrftoken'), 'sessionid': request.COOKIES.get('sessionid')}
    headers = {}
    headers['X-CSRFToken'] = cookies_now['csrftoken']
    response = requests.delete("http://127.0.0.1:8000/api/app/organizations/" + str(org_id), cookies=cookies_now,
                              headers=headers)
    return redirect('/main')

