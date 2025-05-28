from django.shortcuts import render, HttpResponseRedirect
from users.forms import UserLoginForm, UserRegistrationForm
from django.contrib import auth
from django.contrib import messages


# Create your views here.
def login(request):
    if request.method == "POST":
        form = UserLoginForm(data = request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect('/')
        else:
            print(form.errors)
            messages.error(request, "Пожалуйста, исправьте ошибки в форме")
    else:
        form = UserLoginForm()
    context = {
        'form': form
    }
    return render(request, 'users/login.html', context)

def registrarion(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        else:
            print(form.errors)  
    else:
        form = UserRegistrationForm()

    context = {
        'form': form
    }

    return render(request, 'users/reg.html', context)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')