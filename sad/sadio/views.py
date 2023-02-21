from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, "sadio/index.html", {})

def libraries(request):
    return HttpResponse("This is your libraries")

def library(request):
    return HttpResponse("This is x library")
