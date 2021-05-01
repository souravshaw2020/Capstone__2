from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.http import HttpResponse
from app.models import Calculate
from django.db import connection
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
# Create your views here.
#def start(request):
#    if request.method == 'POST':
#        if request.POST.get("log"):
#            return redirect('login')
#        elif request.POST.get("signup"):
#            return render(request,'register.html')
#    else:
#        return render(request,'start.html')
def register(request):
    if request.method == 'POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        password=request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.info(request,'Username already exists')
            return redirect('register')
        else:
            user=User.objects.create_user(username=username,password=password,first_name=first_name,last_name=last_name)
            user.save()
            return redirect('/')
    else:
        return render(request,'signup.html')

def login(request):
    if  request.user.is_authenticated:
            return redirect('/app')
    else:
        if request.method == 'POST':
            username=request.POST['username']
            password=request.POST['password']
            user=auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request,user)
                request.session['username'] = username
                return redirect('/app')
            else:
                messages.info(request,'The credentials are not valid')
                return redirect('/')
        else:
            return render(request,'login.html')

def visitorlogin(request):
    if request.method == 'POST':
        genre=request.POST['genre']
        popular=request.POST['popular']
        if request.POST.get('Generate') == 'Generate':
            if(len(popular)!=0 and len(genre)!=0):
                query="select mname, mgenre from app_avgscore where mgenre like '%%%s%%' limit %s " % (genre, popular)
            elif(len(popular)==0):
                query="select mname, mgenre from app_avgscore where mgenre like '%%%s%%'" % (genre)
            elif(len(genre)==0):
                query="select mname, mgenre from app_avgscore order by mscore desc limit %s" % (popular)
            cursor = connection.cursor()
            cursor.execute(query)
            res= cursor.fetchall()
            return render(request,'genre.html',{'query':res})
    else:
        return render(request,'genre.html')

def top10(request):
    query="select mname, mgenre from app_avgscore order by mscore desc limit 10"
    # vars = _, detected_language['language'].decode("utf8"), str(genre).decode("utf8")
    cursor = connection.cursor()
    cursor.execute(query)
    res= cursor.fetchall()
    print(type(res))
    return render(request,'top10.html',{'query':res})

def trending(request):
    list=["Comedy", "Thriller", "Drama", "Mystery","Action", "Romance", "Horror", "War", "Fantasy"]
    dict={}
    for i in list:
        query="select mname, mgenre from app_avgscore where mgenre like '%%%s%%' order by mscore desc limit 10" % (i)
        # vars = _, detected_language['language'].decode("utf8"), str(genre).decode("utf8")
        cursor = connection.cursor()
        cursor.execute(query)
        res= cursor.fetchall()
        dict[i]=res
    return render(request,'trending.html',{'query':dict})

@login_required(login_url='login')
def logout(request):
    try:
        del request.session['username']
    except:
        pass
    auth.logout(request)
    return HttpResponse("You are logged out")
