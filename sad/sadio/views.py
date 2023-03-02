from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import models

USERNAME_TEXT_INPUT_KEY = "username-text-input"
PASSWORD_PASSWORD_INPUT_KEY = "password-password-input"
LOGIN_SUBMIT_INPUT_KEY = "login-submit-input"
REGISTER_SUBMIT_INPUT_KEY = "register-submit-input"
LOGINED_USER_KEY = "logined_user"
LOGIN_MESSAGE_KEY = ""


def get_user(username):
    users = User.objects.all()
    for user in users:
        if user.username == username:
            return user
    return None


def index(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get(USERNAME_TEXT_INPUT_KEY, None)
        password = request.POST.get(PASSWORD_PASSWORD_INPUT_KEY, None)
        print(username)
        if LOGIN_SUBMIT_INPUT_KEY in request.POST:
            # TODO: Check username and password here
            # retrieve user from database and compare
            print("qwer")
            user = get_user(username)
            print(user)
            if user:
                if user.password == password:
                    request.session[LOGINED_USER_KEY] = username
                    print("You are logged in!")
                    return redirect("libraries")
                else:
                    print("Wrong inputs for login!")
                    pass

        elif REGISTER_SUBMIT_INPUT_KEY in request.POST:
            # TODO: Create user here
            # add user to database
            if not get_user(username):
                record = User(username=username, password=password)
                record.save()
                context[LOGIN_MESSAGE_KEY] = "You are registered!"
            else:
                context[LOGIN_MESSAGE_KEY] = "Wrong inputs for register!"
    return render(request, "sadio/Index.html", context)

def libraries(request):
    context = {}
    logined_user = request.session.get(LOGINED_USER_KEY, None)
    print(logined_user)
    context["logined_user"] = logined_user
    # TODO: Load libraries
    return render(request, "sadio/Libraries.html", context)


def library(request):
    return HttpResponse("This is x library")


def upload_file(file):
    pass

