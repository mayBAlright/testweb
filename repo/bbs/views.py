from django.shortcuts import render, redirect, resolve_url
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import User

# Create your views here.

def register(request):   #회원가입 페이지를 보여주기 위한 함수
    if request.method == "GET":
        return render(request, 'register.html')

    elif request.method == "POST":
        username = request.POST.get('username', None)   #딕셔너리형태
        password = request.POST.get('password', None)
        re_password = request.POST.get('re_password', None)
        res_data = {} 
        if not (username and password and re_password) :
            res_data['error'] = "모든 값을 입력해야 합니다."
            return render(request, 'register.html', res_data)
        if password != re_password :
            # return HttpResponse('비밀번호가 다릅니다.')
            res_data['error'] = '비밀번호가 다릅니다.'
        else :
            user = User(username=username, password=make_password(password))
            user.save()
        return render(request, 'register.html', res_data)

def login(request):
    response_data = {}

    if request.method == "GET" :
        return render(request, 'login.html')

    elif request.method == "POST":
        login_username = request.POST.get('username', None)
        login_password = request.POST.get('password', None)


        if not (login_username and login_password):
            response_data['error']="아이디와 비밀번호를 모두 입력해주세요."
        else : 
            myuser = User.objects.get(username=login_username) 
            #db에서 꺼내는 명령. Post로 받아온 username으로 , db의 username을 꺼내온다.
            if check_password(login_password, myuser.password):
                request.session['user'] = myuser.id 
                #세션도 딕셔너리 변수 사용과 똑같이 사용하면 된다.
                #세션 user라는 key에 방금 로그인한 id를 저장한것.
                return redirect('/')
            else:
                response_data['error'] = "비밀번호를 틀렸습니다."

        return render(request, 'login.html',response_data)

def home(request):
    user_id = request.session.get('user')
    if user_id :
        myuser_info = User.objects.get(pk=user_id)
        return render(request, 'home.html', {
            'user_id': myuser_info
        })   # 로그인을 했다면, username 출력
    else:
        messages.info(request, '로그인이 필요합니다.')
        return HttpResponseRedirect('login/')
    
    
def logout(request):
    user_id = request.session.get('user')
    if user_id :
        request.session.pop('user')
    return redirect('/login/')