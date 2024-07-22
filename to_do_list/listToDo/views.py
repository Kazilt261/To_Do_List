import json
from multiprocessing import context
from re import template
from unittest import loader
from urllib import response
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from .utils.token import generateJWT
from listToDo.models import user as User
import hashlib

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt #Esto es solo para testear, se recomienda quitarlo en producción
def login(request):
    if request.method == "GET":
        return render(request, 'initSession.html')
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email == None or password == None:
            return HttpResponse("Error: missing parameters")
        else:
            user = User.objects.filter(email=email, hash_password_email=hashlib.sha256((password+email).encode()).hexdigest()).first()
            if user == None:
                return JsonResponse({"message": "User not found"})
            request.session['token'] = generateJWT(user.username, user.email, user.hash_password_email)
            return HttpResponse("Hello, world. You're at the polls index.")


@csrf_exempt #Esto es solo para testear, se recomienda quitarlo en producción
def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    if request.method == "POST":
        name = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        hash_object = hashlib.sha256((password+email).encode())
        hex_dig = hash_object.hexdigest()
        user = User(username=name, email=email, hash_password_email=hex_dig)
        try:
            user.save()
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                return JsonResponse({"message": "User already exists"})
            return JsonResponse({"message": str(e)})
            
        return redirect('/users/login')

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