from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth

# Create your views here.




def login(request):
    if request.method =='POST':
        email = request.POST['email'].replace(' ','').lower()
        password = request.POST['password']

        user = auth.authenticate(username=email, password=password)

        if user:
            auth.login(request,user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid Credentials / User doesn't exist")
            return redirect('register')


    return render(request, 'authorization/login.html', {})


def register(request):

    if request.method =='POST':
        email = request.POST['email'].replace(' ','').lower()
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if not password1 ==password2:
            messages.error(request,"Password do not match")
            return redirect(register)

        if User.objects.filter(email=email).exists():
            messages.error(request, "A user with email address: {} already exists, please use a different email".format(email))
            return redirect('register')
    
        user= User.objects.create_user(email=email, username=email, password=password2)
        user.save()
        auth.login(request,user)
        return redirect('dashboard')

        
    return render(request, 'authorization/register.html', {})

def logout(request):
    auth.logout(request)
    return redirect('home')