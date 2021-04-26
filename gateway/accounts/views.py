from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import previousOrders, restra_info
from .rpc import rpc
from datetime import date, datetime, timedelta
# Create your views here.

def index(request):
    return render(request,"index.html")

def hotelPage(request,city_name,hotel_name):
    if request.method == 'GET':
        return render(request,"hotelBook.html", {'hotelName': hotel_name})
    else:
        date_post = datetime.strptime(request.POST['date'],"%Y-%m-%d").date()
        if date_post < dateToday():
            messages.info(request,'Invalid date')
            return redirect('/hotelPage/' + city_name + '/' + hotel_name)
        
        time_post = datetime.strptime(request.POST['time'],"%H:%M").time()
        time_start = datetime.strptime("08:00","%H:%M").time()
        time_end = datetime.strptime("22:00","%H:%M").time()

        if time_post < time_start or time_post > time_end:
            messages.info(request,'Invalid time')
            return redirect('/hotelPage/' + city_name + '/' + hotel_name)
        elif date_post == dateToday() and time_post < timeNow():
            messages.info(request,'Invalid time')
            return redirect('/hotelPage/' + city_name + '/' + hotel_name)
        else:
            response = rpc.cit(hotel_name + ', ' +request.POST['date'] + ', ' + request.POST['seats']).decode()
            if response == "success":
                previousOrders.objects.create(username=request.user.username
                                             ,ordertime=dateTimeNow()
                                             ,hotelname=hotel_name
                                             ,cityname=city_name
                                             ,bookingdate=date_post
                                             ,bookingtime=time_post
                                             )
                return redirect('orderHistory')
            else:
                messages.info(request,'Only ' + response + ' seats are left for this date')
                return redirect('/hotelPage/' + city_name + '/' + hotel_name)

def dateTimeNow():
    return datetime.now() + timedelta(hours=5, minutes=30)

def timeNow():
    now = datetime.now().time()
    nowdt = datetime.combine(datetime.now().date(),now)
    nowdt += timedelta(hours=5, minutes=30)
    return nowdt.time()

def dateToday():
    now = datetime.now() + timedelta(hours=5, minutes=30)
    return now.date()


def logout(request):
    auth.logout(request)
    return redirect('/')

def hotelSearch(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request,"search.html")
        else:
            return redirect('login')
    else:
        cn = request.POST['name']
        rpc_response = rpc.city(cn.lower())
        s = rpc_response
        s = s.decode()
        if s == '[]':
            s = []
        else:
            s = s[2:-2].split('), (')
        response_list = []
        for i in s:
            curr = i[1:-1].split("', '")
            curr = list(map(str, curr))
            res = restra_info()
            res.res_name = curr[0]
            res.res_city = curr[1]
            res.res_type = curr[2]
            response_list.append(res)
        return render(request,"searchResults.html", {'restras': response_list})

def orderHistory(request):
    entries = previousOrders.objects.filter(username=request.user.username)
    return render(request,"orderHistory.html", {'entries': entries})

def login(request):
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['pwd']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect("/")
        else:
            messages.info(request,'Invalid credentials...')
            return redirect('login')
    else:
        return render(request,"login.html")

def register(request):
    if request.method == 'POST':
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        username = request.POST['uname']
        password1 = request.POST['pwd1']
        password2 = request.POST['pwd2']
        email = request.POST['email']
                
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                user.save()
                return redirect('login')
        else:
            messages.info(request,'Passwords not matching')
            return redirect('register')
        return redirect('/')
    else:
        return render(request,"register.html")