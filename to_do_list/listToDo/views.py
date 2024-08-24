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
from listToDo.models import task as Task
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

@csrf_exempt 
def createTask(request):
    if request.method == "POST":
        name=request.POST.get("taskName")
        description=request.POST.get("taskDescription")
        time=request.POST.get("taskLimitTime")
        type=request.POST.get("taskType")
        token = request.COOKIES.get('token')
        if name==None or description==None or time==None:
            return JsonResponse({"message": "Invalid data"},status=400)
        if token == None:
            response=HttpResponse()
            response.status_code=401
            return response
        dataUser = decodeJWT(token)
        if "error" in dataUser:
            response=HttpResponse()
            response.status_code=401
            return response
        user = User.objects.filter(username=dataUser['username']).first()
        if user == None:
            response=HttpResponse()
            response.status_code=401
            return response
        newTask=Task(title=name, description=description, end_date=time, user=user, type=type)
        try:
            newTask.save()
        except Exception as e:
            print(e)
            return JsonResponse({"error": "A"},status=500)
        return JsonResponse({"id":newTask.id},status=201)
    
@csrf_exempt 
def updateTask(request, id):
    if request.method == "PATCH":
        data = json.loads(request.body)
        oldTaskId=id
        token = request.COOKIES.get('token')
        if token == None:
            response=HttpResponse()
            response.status_code=400
            return response
        dataUser = decodeJWT(token)
        if "error" in dataUser:
            response=HttpResponse()
            response.status_code=401
            return response
        user = User.objects.filter(username=dataUser['username']).first()
        if user == None:
            response=HttpResponse()
            response.status_code=401
            return response
        task = Task.objects.filter(id=oldTaskId).first()
        print(task.description)
        if oldTaskId == None:
            response=HttpResponse()
            response.status_code=401
            return response
        if task.user!=user:
            response=HttpResponse()
            response.status_code=401
            return response
        try:
            if "name" in data:
                task.title=data["name"]
            if "description" in data:
                task.description=data["description"]
            if "time" in data:
                task.end_date=data["time"]
            if "type" in data:
                task.type=data["type"]
            if "status" in data:
                task.status = bool(data["status"])

            task.save()
        except Exception as e:
            return JsonResponse({"error": e},status=500)
        return JsonResponse({},status=202)
@csrf_exempt 
def deleteTask(request, id):
    if request.method == "DELETE":
        idTask=id
        token = request.COOKIES.get('token')
        if idTask==None:
            return JsonResponse({"message": "Invalid data"},status=400)
        if token == None:
            response=HttpResponse()
            response.status_code=400
            return response
        dataUser = decodeJWT(token)
        if "error" in dataUser:
            response=HttpResponse()
            response.status_code=401
            return response
        user = User.objects.filter(username=dataUser['username']).first()
        if user == None:
            response=HttpResponse()
            response.status_code=401
            return response
        task = Task.objects.filter(id=idTask).first()
        if task == None:
            response=HttpResponse()
            response.status_code=404
            return response
        if task.user!=user:
            response=HttpResponse()
            response.status_code=401
            return response
        try:
            task.delete()
        except Exception as e:
            print(e)
            return JsonResponse({"error": "A"},status=500)
        return JsonResponse({},status=201)

def listTask(request,page= 1):
    if request.method == "GET":
        token = request.COOKIES.get('token')
        if token == None:
            response=HttpResponse()
            response.status_code=401
            return response
        dataUser = decodeJWT(token)
        if "error" in dataUser:
            response=HttpResponse()
            response.status_code=401
            return response
        user = User.objects.filter(username=dataUser['username']).first()
        if user == None:
            response=HttpResponse()
            response.status_code=401
            return response
        tasks = Task.objects.filter(user=user,).order_by('end_date')
        tasksList = []
        for task in tasks:
            tasksList.append({"id":task.id, "title":task.title, "end_date":task.end_date, "status":task.status})
        return JsonResponse({"tasks":tasksList, "more":False},status=200)
    return

def detailTask(request, id):
    if request.method == "GET":
        token = request.COOKIES.get('token')
        if token == None:
            response=HttpResponse()
            response.status_code=401
            return response
        dataUser = decodeJWT(token)
        if "error" in dataUser:
            response=HttpResponse()
            response.status_code=401
            return response
        user = User.objects.filter(username=dataUser['username']).first()
        if user == None:
            response=HttpResponse()
            response.status_code=401
            return response
        task = Task.objects.filter(id=id).first()
        if task == None:
            response=HttpResponse()
            response.status_code=404
            return response
        if task.user!=user:
            response=HttpResponse()
            response.status_code=401
            return response
        return JsonResponse({"id":task.id, "title":task.title, "description":task.description, "end_date":task.end_date, "status":task.status},status=200)

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