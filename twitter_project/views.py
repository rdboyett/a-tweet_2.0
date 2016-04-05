import json

from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.mail import send_mail

#from userInfo_profile.models import UserInfo, MyAnswer, MyGrade
from classrooms.models import ClassUser, Classroom, HashTag, Message
from google_login.models import GoogleUserInfo
from userInfo_profile.models import UserInfo



def index(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        if User.objects.filter(id=user_id):
            user = User.objects.get(id=user_id)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return HttpResponseRedirect("/dashboard/")
        
        else:
            user_id = False
    else:
        return redirect('/google/auth/')



@login_required
def dashboard(request, classID=False):
    if ClassUser.objects.filter(user=request.user):
        userInfo = ClassUser.objects.get(user=request.user)
    
    
    #get avatar and background images:
    if UserInfo.objects.filter(user=request.user):
        userImages = UserInfo.objects.get(user=request.user)
    else:
        userImages = False
    
    
    #Get total number of tweets made by user.
    if userInfo.messages.all():
        tweetCount = userInfo.messages.all().count()
    else:
        tweetCount = 0;
        
    #Get all users classes
    if userInfo.classrooms.all():
        allClasses = userInfo.classrooms.all().order_by('name')
    else:
        allClasses = False
        
    
    #Get Trending for the class
    if classID:
        if HashTag.objects.filter(classroomID=classID):
            trendings = HashTag.objects.filter(classroomID=classID).order_by('-timeDate')[:20]
        else:
            trendings = False
    elif allClasses:
        if HashTag.objects.filter(classroomID=allClasses[0].id):
            trendings = HashTag.objects.filter(classroomID=allClasses[0].id).order_by('-timeDate')[:20]
        else:
            trendings = False
    else:
        trendings = False
        
    
    #Get Current Class
    if classID:
        if Classroom.objects.filter(id=classID):
            currentClass = Classroom.objects.get(id=classID)
        else:
            currentClass = False
    elif allClasses:
        currentClass = allClasses[0]
    else:
        currentClass = False
        
    
    #Get Tweets
    if currentClass:
        if currentClass.messages.all():
            tweets = currentClass.messages.all().order_by('-timeDate')[0:20]
        else:
            tweets = False
    else:
        tweets = False
    
    args = {
            'user':request.user,
            'userInfo':userInfo,
            'userImages':userImages,
            'tweetCount':tweetCount,
            'allClasses':allClasses,
            'trendings':trendings,
            'currentClass':currentClass,
            'tweets':tweets,
            'dashboard':True,
        }
    args.update(csrf(request))
    
    return render_to_response("dashboard.html", args)






@login_required
def profile(request):
    if ClassUser.objects.filter(user=request.user):
        userInfo = ClassUser.objects.get(user=request.user)
    
    #get avatar and background images:
    if UserInfo.objects.filter(user=request.user):
        userImages = UserInfo.objects.get(user=request.user)
    else:
        userImages = False
    
    #Get total number of tweets made by user.
    if userInfo.messages.all():
        myMessages = userInfo.messages.all().order_by('-timeDate')[:20]
        tweetCount = myMessages.count()
    else:
        myMessages = False
        tweetCount = 0;
        
    #Get all users classes
    if userInfo.classrooms.all():
        allClasses = userInfo.classrooms.all().order_by('name')
    else:
        allClasses = False
        
    
    
    args = {
            'user':request.user,
            'userInfo':userInfo,
            'userImages':userImages,
            'tweetCount':tweetCount,
            'allClasses':allClasses,
            'tweets':myMessages,
            'profile':True,
        }
    args.update(csrf(request))
    
    return render_to_response("profile.html", args)
































