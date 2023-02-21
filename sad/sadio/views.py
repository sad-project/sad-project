from django.shortcuts import render
from django.http import HttpResponse

from .lib.libhandler import create_library

def index(request):
    return render(request, "sadio/index.html", {})

def libraries(request):
    return HttpResponse("This is your libraries")

def library(request):
    return HttpResponse("This is x library")
