import json
from multiprocessing import context
from re import template
from unittest import loader
from urllib import response
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from utils.token import generateJWT, decodeJWT
import utils.validator as validator
from listToDo.models import user as User
import hashlib

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt #Esto es solo para testear, se recomienda quitarlo en producción
def login(request):
    if request.method == "GET":
        if request.COOKIES.get('token') == None:
            return render(request, 'initSession.html')
        dataUser = decodeJWT(request.COOKIES.get('token'))
        if dataUser == None:
            return render(request, 'initSession.html')
        user = User.objects.filter(username=dataUser['username']).first()
        if user == None:
            response = redirect('/users/login')
            response.delete_cookie('token')
            return response
        return redirect('/')
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email == None or password == None:
            return JsonResponse({"message": "Invalid credentials"},status=401)
        user = User.objects.filter(email=email, hash_password_email=hashlib.sha256((password+email).encode()).hexdigest()).first()
        if user == None:
            return JsonResponse({"message": "Invalid credentials"},status=401)
        response = JsonResponse({})
        response.set_cookie('token', generateJWT(user.username, user.email, user.hash_password_email))
        return response


@csrf_exempt #Esto es solo para testear, se recomienda quitarlo en producción
def register(request):
    if request.method == "GET":
        if request.COOKIES.get('token') == None:
            return render(request, 'register.html')
        dataUser = decodeJWT(request.COOKIES.get('token'))
        if dataUser == None:
            return render(request, 'register.html')
        user = User.objects.filter(username=dataUser['username']).first()
        if user == None:
            response = redirect('/users/register')
            response.delete_cookie('token')
            return response
        return redirect('/')
    if request.method == "POST":
        name = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if name == None or email == None or password == None:
            return JsonResponse({"message": "Invalid data"},status=400)

        if validator.validateEmail(email) == False:
            return JsonResponse({"error": "email", "details":"Invalid email"},status=400)
        if validator.validateUserName(name) != "":
            return JsonResponse({"error": "username", "details":validator.validateUserName(name)},status=400)
        if validator.validatePassword(password) != "":
            return JsonResponse({"error": "password", "details":validator.validatePassword(password)},status=400)   

        hash_object = hashlib.sha256((password+email).encode())
        hex_dig = hash_object.hexdigest()
        user = User(username=name, email=email, hash_password_email=hex_dig)
        try:
            user.save()
        except Exception as e:
            if "UNIQUE constraint failed: listToDo_user.username" in str(e):
                print(e)
                return JsonResponse({"error": "username", "details":"This username already exists"},status=400)
            if "UNIQUE constraint failed: listToDo_user.email" in str(e):
                print(e)
                return JsonResponse({"error": "email","details":"This email already exists"},status=400)
            return JsonResponse({"message": "Error creating user"},status=500)
        return JsonResponse({},status=201)
    
def logout(request):
    response = redirect('/users/login')
    response.delete_cookie('token')
    return response

def createTask(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def updateTask(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def deleteTask(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def listTasks(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def index(request):
    if request.method == "GET":
        token = request.COOKIES.get('token')
        if token == None:
            return redirect('/users/login')
        dataUser = decodeJWT(token)
        if "error" in dataUser:
            request.session['token'] = None
            return redirect('/users/login')
        user = User.objects.filter(username=dataUser['username']).first()
        if user == None:
            response = redirect('/users/login')
            response.delete_cookie('token')
            return response
        
        return render(request, 'index.html',{'username': user.username, 'email': user.email})