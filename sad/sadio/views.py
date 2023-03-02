from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Library, User
from .lib.libhandler import LibraryHandler
import os

USERNAME_TEXT_INPUT_KEY = "username-text-input"
PASSWORD_PASSWORD_INPUT_KEY = "password-password-input"
LOGIN_SUBMIT_INPUT_KEY = "login-submit-input"
REGISTER_SUBMIT_INPUT_KEY = "register-submit-input"
LOGINED_USER_KEY = "logined_user"
LOGIN_MESSAGE_KEY = ""
CREATE_LIBRARY_SUBMIT_INPUT_KEY = "create-library-submit-input"
LIBRARY_NAME_TEXT_INPUT_KEY = "library-name-text-input"
FILE_INPUT_KEY = "file-input"
UPLOAD_FILE_SUBMIT_INPUT_KEY = "upload-file-submit-input"

libraryhandler = LibraryHandler()

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
    logined_user = request.session.get(LOGINED_USER_KEY, "Default User")
    context["logined_user"] = logined_user
    user = User.objects.get(username=logined_user)
    libraries = Library.objects.filter(owner=logined_user)
    context["libraries"] = libraries
    if request.method == 'POST':
        if CREATE_LIBRARY_SUBMIT_INPUT_KEY in request.POST:
            library_name = request.POST.get(LIBRARY_NAME_TEXT_INPUT_KEY, None)
            if library_name:
                bucket = libraryhandler.create_new_bucket()
                library = Library(name=library_name, owner=user, bucket=bucket, fields={})
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

