from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        pwd = request.POST['pwd']
        
        user = auth.authenticate(username=username, password=pwd) 

        if user is not None:
            auth.login(request,user)
            print(request.user)
            return redirect('calendar')
        else:
            messages.info(request, "Username or Password Doesnt exist")
            return redirect('login')
    else:
        return render(request , 'login.html')


def register(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        pwd = request.POST['pwd']
        cpwd = request.POST['cpwd']

        if pwd == cpwd:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('login')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('login')
            else:
                user = User.objects.create_user(username=username, password=pwd, email=email, first_name=firstname, last_name=lastname)
                user.save()
                return redirect('login')
        else:
            messages.info(request, "Password doesnt match")
            return redirect('login')
    
        return redirect('/')
    else:
        return render(request, 'login.html')
    
@login_required
def logoutview(request):
    auth.logout(request)
    return redirect('/')