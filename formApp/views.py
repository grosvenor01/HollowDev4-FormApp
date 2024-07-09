from django.shortcuts import render , redirect
from .models import *
from django.contrib.auth import authenticate , login
from collections import defaultdict
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method =="GET":
        return render(request, "register.html")
    if request.method == "POST":
        try : 
            username=request.POST.get("username")
            Email = request.POST.get("email")
            password = request.POST.get("password")
            if len(password)<8:
                return render(request, "register.html",context={"Error":"password should be minimum 8 carecters"})
            user = User.objects.create_user(username=username , password=password , email = Email)
            user.save()
            return render(request, "login.html")
        except Exception as e:
            print(e)
            return render(request, "register.html",context={"Error":"Error occured try change the username or email"})

def loging(request):
    if request.method == "GET":
        return render(request, "login.html")
    if request.method =="POST":
        username=request.POST.get("username")
        password = request.POST.get("password")
        user= authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            user = User.objects.get(username=username)
            response =redirect("/")
            response.set_cookie('username', username, max_age=360000)
            return response
        else :
            return render(request, "login.html",context={"Error":"you can't login with this credentials"})

@login_required(login_url='/login/')
def home(request):
    if request.method =="GET":
        user = User.objects.get(username=request.COOKIES.get("username"))
        formes = form.objects.filter(owner=user)
        context={
            "forms" : formes
        }
        return render(request , "buildForm.html" , context=context)
    if request.method =="POST":
        # getting number of question 
        data = request.POST
        question_count = 0
        for key, value in data.items():
            parts = key.split('-')
            if len(parts) == 3 and parts[0] == 'question':
                question_number = int(parts[1])
                question_count = max(question_count, question_number)
        # create ne form
        forme = form.objects.create(name="form of "+request.COOKIES.get("username") , owner = User.objects.get(username=request.COOKIES.get("username") ))
        forme.save()
        # save the questions 
        print(data)
        for i in range(question_number):
            questionn = request.POST.get("question-"+str(i+1))
            question_type = request.POST.get("question-"+str(i+1)+"-type")
            print(question_type)
            if question_type =="option":
                options=[]
                for j in range(4):
                    options.append(request.POST.get("question-"+str(i+1)+"-option-"+str(j+1)))
                question_to_save = question.objects.create(
                    form=forme,
                    type="Option",
                    question=questionn, 
                    option1=options[0],
                    option2=options[1],
                    option3=options[2],
                    option4=options[3],
                    question_number=i+1
                )
                question_to_save.save()
            else :
                question_to_save= question.objects.create(
                    form=forme,
                    type="Text",
                    question_number=i+1,
                    question = questionn
                )
                question_to_save.save()

        return render(request , "copylink.html" , context={"id":forme.id})

@login_required(login_url='/login/')
def response_view(request , id ):
    if request.method == "GET":
        forme =form.objects.get(id=id)
        questions = question.objects.filter(form = forme).order_by("question_number")
        context ={
            "form":forme,
            "questions":questions
        }
        return render(request , "response.html", context=context)
    elif request.method == "POST" :
        data = request.POST
        question_count = 0
        for key, value in data.items():
            parts = key.split('-')
            if len(parts) == 2 and parts[0] == 'question':
                question_number = int(parts[1])
                question_count = max(question_count, question_number)
        user = User.objects.get(username=request.COOKIES.get("username"))
        for i in range(question_count):
            response_to_save = Respons.objects.create(
                user=user , 
                question=question.objects.get(form__id=id,question_number=i+1),
                answer = request.POST.get("question-"+str(i+1))
            )
            response_to_save.save()
        return redirect("home")
    
@login_required(login_url='/login/')
def responses_view(request, id):
    forme = form.objects.get(id=id)
    questions = question.objects.filter(form=forme).order_by("question_number")
    responses = []

    for questionn in questions:
        answers = Respons.objects.filter(question=questionn)
        for answerr in answers:
            response_data = {
                "username":answerr.user.username,
                "question": questionn.question,
                "answer": answerr.answer
            }
            responses.append(response_data)

    context = {"responses": responses}
    print(context)
    return render(request, "Responses.html", context=context)