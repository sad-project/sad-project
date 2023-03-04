from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Library, User
from .userlib.libhandler import LibraryHandler
import os

LOGIN_USERNAME_TEXT_INPUT_KEY = "login-username-text-input"
LOGIN_PASSWORD_PASSWORD_INPUT_KEY = "login-password-password-input"
REGISTER_USERNAME_TEXT_INPUT_KEY = "register-username-text-input"
REGISTER_PASSWORD_PASSWORD_INPUT_KEY = "register-password-password-input"
REGISTER_CONFIRM_PASSWORD_PASSWORD_INPUT_KEY = "register-confirm-password-password-input"
LOGIN_SUBMIT_INPUT_KEY = "login-submit-input"
REGISTER_SUBMIT_INPUT_KEY = "register-submit-input"
LOGINED_USER_KEY = "logined_user"
LOGIN_MESSAGE_KEY = "login_message"
CREATE_LIBRARY_SUBMIT_INPUT_KEY = "create-library-submit-input"
LIBRARY_NAME_TEXT_INPUT_KEY = "library-name-text-input"
FILE_INPUT_KEY = "file-input"
UPLOAD_FILE_SUBMIT_INPUT_KEY = "upload-file-submit-input"

libraryhandler = LibraryHandler()


def index(request):
    context = {}
    if request.method == 'POST':
        if LOGIN_SUBMIT_INPUT_KEY in request.POST:
            username = request.POST.get(LOGIN_USERNAME_TEXT_INPUT_KEY, None)
            password = request.POST.get(
                LOGIN_PASSWORD_PASSWORD_INPUT_KEY, None)
            user = get_user(username)
            if user:
                if user.password == password:
                    request.session[LOGINED_USER_KEY] = username
                    return redirect("libraries")
                else:
                    context[LOGIN_MESSAGE_KEY] = "Wrong password"
            else:
                context[LOGIN_MESSAGE_KEY] = "User not found"
        elif REGISTER_SUBMIT_INPUT_KEY in request.POST:
            username = request.POST.get(REGISTER_USERNAME_TEXT_INPUT_KEY, None)
            password = request.POST.get(
                REGISTER_PASSWORD_PASSWORD_INPUT_KEY, None)
            password_confirm = request.POST.get(
                REGISTER_CONFIRM_PASSWORD_PASSWORD_INPUT_KEY, None)
            user = get_user(username)
            if user:
                context[LOGIN_MESSAGE_KEY] = "Username already exists"
            else:
                if password == password_confirm and password != None and password != "":
                    new_user = User(username=username, password=password)
                    new_user.save()
                    context[LOGIN_MESSAGE_KEY] = "User created successfuly"
    return render(request, "sadio/Index.html", context)


def libraries(request):
    context = {}
    logined_user = request.session.get(LOGINED_USER_KEY, "Default User")
    context["logined_user"] = logined_user
    user = get_user(logined_user)
    libraries = Library.objects.filter(owner=logined_user)
    context["libraries"] = libraries
    if request.method == 'POST':
        if CREATE_LIBRARY_SUBMIT_INPUT_KEY in request.POST:
            library_name = request.POST.get(LIBRARY_NAME_TEXT_INPUT_KEY, None)
            if library_name:
                bucket = libraryhandler.create_new_bucket()
                library = Library(name=library_name, owner=user,
                                  bucket=bucket, fields={})
                library.save()
                return redirect("libraries")

    return render(request, "sadio/Libraries.html", context)


def library(request, library_name: str):
    context = {}
    library = Library.objects.get(name=library_name)
    if request.method == 'POST':
        if UPLOAD_FILE_SUBMIT_INPUT_KEY in request.POST:
            file = request.FILES[FILE_INPUT_KEY]
            with open(file.name, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            libraryhandler.upload_file(library.bucket, file.name)
            os.remove(file.name)
    context["library"] = library
    context["files"] = libraryhandler.get_file_list(library.bucket)
    return render(request, "sadio/Library.html", context)


def upload_file(file):
    pass



def get_user(username):
    try:
        return User.objects.get(username=username)
    except:
        return None