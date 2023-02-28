from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import models

USERNAME_TEXT_INPUT_KEY = "username-text-input"
PASSWORD_PASSWORD_iNPUT_KEY = "password-password-input"
LOGIN_SUBMIT_INPUT_KEY = "login-submit-input"
REGISTER_SUBMIT_INPUT_KEY = "register-submit-input"
LOGINED_USER_KEY = "logined_user"


def index(request):
    if request.method == 'POST':
        username = request.POST.get(USERNAME_TEXT_INPUT_KEY, None)
        password = request.POST.get(PASSWORD_PASSWORD_iNPUT_KEY, None)
        if LOGIN_SUBMIT_INPUT_KEY:
            # TODO: Check username and password here
            # if username == 
            # retrieve user from database and compare
            request.session[LOGINED_USER_KEY] = username
            users = User.objects.all()
            return redirect("libraries")
        elif REGISTER_SUBMIT_INPUT_KEY:
            # TODO: Create user here
            # add user to database

            pass
    return render(request, "sadio/index.html")


def libraries(request):
    context = {}
    logined_user = request.session.get(LOGINED_USER_KEY, None)
    print(logined_user)
    context["logined_user"] = logined_user
    # TODO: Load libraries
    return render(request, "sadio/libraries.html", context)


def library(request):
    return HttpResponse("This is x library")
