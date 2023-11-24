from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
from .forms import UserSignup, UserSignin
from django.contrib.auth.decorators import login_required


# signup conditions
def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
      

    else:
     if request.method == 'POST':
        fmsp = UserSignup(request.POST)
        if fmsp.is_valid():
            username = fmsp.cleaned_data['username']
            ftname = fmsp.cleaned_data['first_name']
            ltname = fmsp.cleaned_data['last_name']
            pw = fmsp.cleaned_data['password']
            pw2 = fmsp.cleaned_data['Confirm_password']
            if pw == pw2:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Username already exists')
                    return redirect('signup')
                else:
                    registration = User.objects.create_user(
                        username=username, first_name=ftname, last_name=ltname, password=pw)
                    registration.save()
                    messages.info(request, 'Succefully Created your Account')
                    return redirect('signin')
            else:
                messages.info(request, 'Password not match')
                return redirect('signup')
     else:
        fmsp = UserSignup()
    return render(request, '/signup.html/', {'form': fmsp})

    


# signin conditions

@never_cache
def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')

            else:
                messages.error(request, 'Incorrect Username or Password')
                return redirect('signin')
        fmsn = UserSignin()
        return render(request, '/signin.html/', {'form': fmsn})


# home conditions if user authenticated 

@login_required(login_url='signin')
def home(request):
    if request.user.is_authenticated:
        dst = Destination.objects.all()
        return render(request, "/index.html/", {'dst' : dst})
    else:
        return redirect('signin')               
        



# logout condition

@never_cache
@login_required(login_url='signin')
def signout(request):
    logout(request)
    messages.success(request, "Logout successfully")
    return redirect('signin')
