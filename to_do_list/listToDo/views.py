from multiprocessing import context
from re import template
from unittest import loader
from urllib import response
from django.http import HttpResponse
from django.shortcuts import redirect, render



def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def pageInitSession(request):
    if request.method == "GET":
        return render(request, 'initSession.html')
    else:
        return HttpResponse("aqui no bro.")

def initSession(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if username == None or email == None or password == None:
            return HttpResponse("Error: missing parameters")
        else:
            user = user.objects.get(username=username, email=email, hash_password_email=password)
            if user == None:
                return response("Error: user not found")
            return HttpResponse("Hello, world. You're at the polls index.")
    return redirect('index')

def pageRegister(request):
    if request.method == "GET":
        return render(request, 'register.html')
    else:
        return HttpResponse("aqui no bro.")
    

def register(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def login(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def logout(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def createTask(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def updateTask(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def deleteTask(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def listTasks(request):
    return HttpResponse("Hello, world. You're at the polls index.")