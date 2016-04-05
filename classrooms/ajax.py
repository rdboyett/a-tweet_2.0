import json
import re
import os
import errno

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


from classrooms.models import ClassUser, Classroom, HashTag, Message
from classrooms.views import generateCode
from userInfo_profile.models import UserInfo


import logging
log = logging.getLogger(__name__)



try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


try:
    from PIL import Image
except ImportError:
    import Image
    
from twitter_project import settings
ROOT_PATH = settings.ROOT_PATH


@login_required
def createGroup(request):
    if request.method == 'POST':
        userInfo = ClassUser.objects.get(user=request.user)
        groupName = request.POST['group_name'].strip()
        groupCode = generateCode()
                
        classroom = Classroom.objects.create(
            name = groupName,
            code = groupCode,
            classOwnerID = userInfo.id,
        )
        userInfo.classrooms.add(classroom)
        
        data = {'groupID':classroom.id}
        #log.info("GroupName: "+str(groupName)+ " and GroupCode: "+str(groupCode))
    else:
        data = {'error':"didn't work"}
                
    return HttpResponse(json.dumps(data))



@login_required
def deleteGroup(request):
    if request.method == 'POST':
        classID = request.POST["myGroups"]
        #log.info("classID: "+str(classID))
        
        userInfo = ClassUser.objects.get(user=request.user)
                
        if Classroom.objects.filter(id=classID):
            classRoom = Classroom.objects.get(id=classID)
            
            if userInfo.id == classRoom.classOwnerID:
                #delete all the hashtags associated with this classroom
                if HashTag.objects.filter(classroomID=classID):
                    HashTag.objects.filter(classroomID=classID).delete()
                
                #delete all the tweets with this classroom
                if classRoom.messages.all():
                    classRoom.messages.all().delete()
                    
                #delete the classroom
                classRoom.delete()
                
            else:
                userInfo.classrooms.remove(classRoom)
                
            data = {
                    'classID': classID,
                }
        else:
            data = {
                'error': "There is no class by that id",
            }
    else:
        data = {
            'error': "There was an error posting this request. Please try again.",
        }
            
    return HttpResponse(json.dumps(data))




@login_required
def changeGroupName(request):
    if request.method == 'POST':
        classID = request.POST["groupID"]
        group_name = request.POST["group_name"].strip()
        #log.info("classID: "+str(classID))
        
        if Classroom.objects.filter(id=classID):
            classRoom = Classroom.objects.get(id=classID)
            classRoom.name = group_name
            classRoom.save()
            
            data = {
                'groupID': classID,
            }
        else:
            data = {
                'error': "There is no class by that id",
            }
    else:
        data = {
            'error': "There was an error posting this request. Please try again.",
        }
            
    return HttpResponse(json.dumps(data))





@login_required
def toggleLockGroup(request):
    if request.method == 'POST':
        classID = request.POST["groupID"]
        #log.info("classID: "+str(classID))
        
        if Classroom.objects.filter(id=classID):
            classRoom = Classroom.objects.get(id=classID)
            
            if classRoom.allowJoin:
                classRoom.allowJoin = False
            else:
                classRoom.allowJoin = True
                
            classRoom.save()
            
            data = {
                'allowJoin': classRoom.allowJoin,
            }
        else:
            data = {
                'error': "There is no class by that id",
            }
    else:
        data = {
            'error': "There was an error posting this request. Please try again.",
        }
            
    return HttpResponse(json.dumps(data))



@login_required
def joinGroup(request):
    if request.method == 'POST':
        joinCode = request.POST["groupCode"].strip()
        #log.info("classID: "+str(classID))
        
        
        userInfo = ClassUser.objects.get(user=request.user)
                
        #Get all users classes
        if userInfo.classrooms.all():
            allClasses = userInfo.classrooms.all()
        else:
            allClasses = False
        
        
        #get the the class with that joinCode
        if Classroom.objects.filter(code=joinCode):
            newClass = Classroom.objects.get(code=joinCode)
            
                
            if allClasses and newClass in allClasses:
                data = {'error': "Sorry, you already have this class.",}
            else:
                #check to see if you are allowed to join
                if newClass.allowJoin:
                    userInfo.classrooms.add(newClass)
                    data = {
                        'groupID': newClass.id,
                    }
                else:
                    data = {'error': "Sorry, this class is locked by the owner.",}
            
            
            
            
        else:
            data = {'error': "Sorry, there are no classes with that code.",}
    else:
        data = {
            'error': "There was an error posting this request. Please try again.",
        }
            
    return HttpResponse(json.dumps(data))




@login_required
def postMessage(request):
    if request.method == 'POST':
        tweetText = request.POST["post_message"].strip()
        classroomID = request.POST["classID"]
        
        userInfo = ClassUser.objects.get(user=request.user)
        currentClass = Classroom.objects.get(id=classroomID)
        
        #Scrub hashtags out
        reg = re.compile(r'(?:^|\s)[#?](\S*)')
        hashTagList = re.findall(reg, tweetText)
        
        #Save the message
        newTweet = Message.objects.create(
            text = tweetText,
        )
        
        currentClass.messages.add(newTweet)
        userInfo.messages.add(newTweet)
        
        #Save the hashtag individually and point it back to the messages its found in.
        if hashTagList:
            for tag in hashTagList:
                if HashTag.objects.filter(tag=tag):
                    newHashTag = HashTag.objects.get(tag=tag)
                else:
                    newHashTag = HashTag.objects.create(
                        tag = tag,
                        classroomID = classroomID,
                    )
                    
                newHashTag.messages.add(newTweet)
        
        return render_to_response('post_message.html', {
            'message':newTweet,
            'groupID':classroomID,
            'userInfo':userInfo,
        } )
        data = {
            'success': 'True',
            'tweetID': newTweet.id,
            'tweetText': tweetText,
        }
    
    else:
        data = {'error':'Did not post correctly',}
            
    return HttpResponse(json.dumps(data))



@login_required
def deleteMessage(request):
    if request.method == 'POST':
        tweetID = request.POST["messageID"]
        
        userInfo = ClassUser.objects.get(user=request.user)
        
        if Message.objects.filter(id=tweetID):
            oldTweet = Message.objects.get(id=tweetID)
            
            #delete any records for hashtags
            if HashTag.objects.filter(messages=oldTweet):
                hashTagList = HashTag.objects.filter(messages=oldTweet)
                for hashTag in hashTagList:
                    hashTag.messages.remove(oldTweet)
                    if hashTag.messages.all().count() == 0:
                        hashTag.delete()
                        
                    
            userInfo.messages.remove(oldTweet)
            
            for classRoom in oldTweet.classroom_set.all():
                classRoom.messages.remove(oldTweet)
            
            oldTweet.delete()
                    
            data = {
                    'success': 'success',
                    'messageID': tweetID,
                }
                
        
        else:
            data = {
                'error': "Oh no! I can't find that darn message anywhere!",
            }
    else:
        data = {
            'error': "There was an error posting this request. Please try again.",
        }
        
            
    return HttpResponse(json.dumps(data))

'''
@login_required
def addAdminUsers(request):
    if request.method == 'POST':
        userEmail = request.POST["userEmail"]
        
        emailEnding = userEmail.split("@")[1]
        
        if 'alvaradoisd.net' in emailEnding:
            if 'student' not in emailEnding:
                #get user
                if User.objects.filter(email=userEmail):
                    adminUser = User.objects.get(email=userEmail)
                    #create them an admin account
                    if AIS_admin.objects.filter(user=adminUser):
                        return HttpResponse(json.dumps({'error':"Sorry, that person is already a board administrator."}))
                    else:
                        AIS_admin.objects.create(user=adminUser)
                        
                    data = {
                        'success': 'success',
                    }
                else:
                    return HttpResponse(json.dumps({'error':"Either you typed the email wrong or that person has not created an account yet. Let'em know what's up!"}))
            else:
                return HttpResponse(json.dumps({'error':"What are you crazy?!  Students can't be board administrators."}))
        else:
            return HttpResponse(json.dumps({'error':"What are you crazy?!  Only Alvarado ISD employee's can be board administrators."}))
    else:
        data = {
            'error': "There was an error posting this request. Please try again.",
        }
        
            
    return HttpResponse(json.dumps(data))
'''

@login_required
def addAdminUsers(request):
    pass

'''
@login_required
def adminDeleteUser(request):
    if request.method == 'POST':
        adminUserID = request.POST["adminUser"]
        
        if AIS_admin.objects.filter(id=adminUserID):
            AIS_admin.objects.get(id=adminUserID).delete()
            data={'adminUserID':adminUserID}
        else:
            return HttpResponse(json.dumps({'error':"Sorry, something went wrong."}))
    else:
        data = {
            'error': "There was an error posting this request. Please try again.",
        }
        
            
    return HttpResponse(json.dumps(data))
'''

@login_required
def adminDeleteUser(request):
    pass


@login_required
def editProfile(request):
    if request.method == 'POST':
        userFirstName = request.POST["userFirstName"].strip()
        background_color = request.POST["background_color"]
        text_color = request.POST["text_color"]
        
        if ClassUser.objects.filter(user=request.user):
            classUser = ClassUser.objects.get(user=request.user)
            classUser.user.first_name = userFirstName
            classUser.user.save()
            classUser.avatarBackColor = background_color
            classUser.avatarTextColor = text_color
            classUser.save()
            
            data={'success':'success'}
            
        else:
            return HttpResponse(json.dumps({'error':"Sorry, something went wrong."}))
    else:
        data = {
            'error': "There was an error posting this request. Please try again.",
        }
        
            
    return HttpResponse(json.dumps(data))




@login_required
def getOldMessages(request):
    if request.method == 'POST':
        lastMessageID = request.POST["lastMessageID"]
        classroomID = request.POST["groupID"]
        
        userInfo = ClassUser.objects.get(user=request.user)
        currentClass = Classroom.objects.get(id=classroomID)
        
        lastMessage = get_object_or_404(Message, id=lastMessageID)
        
        if Message.objects.filter(classroom__id=classroomID, timeDate__lte=lastMessage.timeDate):
            nextMessages = Message.objects.filter(classroom__id=classroomID, timeDate__lte=lastMessage.timeDate).order_by('-timeDate')[1:21]
        else:
            nextMessages = False
            
        return render_to_response('get_messages.html', {
            'messages':nextMessages,
            'userInfo':userInfo,
        } )
    
    else:
        data = {'error':'Did not post correctly',}
            
    return HttpResponse(json.dumps(data))



@login_required
def getNewMessages(request):
    if request.method == 'POST':
        firstMessageID = request.POST["firstMessageID"]
        classroomID = request.POST["groupID"]
        
        userInfo = ClassUser.objects.get(user=request.user)
        currentClass = Classroom.objects.get(id=classroomID)
        
        firstMessage = get_object_or_404(Message, id=firstMessageID)
        
        if Message.objects.filter(classroom__id=classroomID, timeDate__lte=firstMessage.timeDate):
            nextMessages = Message.objects.filter(classroom__id=classroomID, timeDate__gte=firstMessage.timeDate).order_by('timeDate')[1:21]
        else:
            nextMessages = False
            
        return render_to_response('get_messages.html', {
            'messages':nextMessages,
            'userInfo':userInfo,
        } )
    
    else:
        data = {'error':'Did not post correctly',}
            
    return HttpResponse(json.dumps(data))




@login_required
def changeGroupCode(request):
    if request.method == 'POST':
        userInfo = ClassUser.objects.get(user=request.user)
        groupID = request.POST['groupID'].strip()
        groupCode = generateCode()
                
        if Classroom.objects.filter(id=groupID):
            classroom = Classroom.objects.get(id=groupID)
            classroom.code = groupCode
            classroom.save()
            
        
        data = {'groupCode':classroom.code}
        #log.info("GroupName: "+str(groupName)+ " and GroupCode: "+str(groupCode))
    else:
        data = {'error':"didn't work"}
                
    return HttpResponse(json.dumps(data))



@login_required
def addTeacherSchool(request):
    if request.method == 'POST':
        userInfo = ClassUser.objects.get(user=request.user)
        school = request.POST['school'].strip()
                
        userInfo.school = school
        userInfo.save()
        
        data = {'success':'success'}
        #log.info("GroupName: "+str(groupName)+ " and GroupCode: "+str(groupCode))
    else:
        data = {'error':"didn't work"}
                
    return HttpResponse(json.dumps(data))




def avatarFilePath(filename=None, user=None, avatarName=None):
    fileExtension = filename.split('.')[1]
    make_sure_path_exists(os.path.join(ROOT_PATH,'media','avatars', user.username))
    return os.path.join('media','avatars', user.username, avatarName)


@login_required
def avatarCrop(request):
    if request.method == 'POST':
        imageFile = request.FILES["image"]
        topPercent = request.POST["topPercent"]
        leftPercent = request.POST["leftPercent"]
        bottomPercent = request.POST["bottomPercent"]
        rightPercent = request.POST["rightPercent"]
        
        path = avatarFilePath(user=request.user, 
            filename=request.FILES['image'].name, avatarName='avatar.jpg')
        
        
        if UserInfo.objects.filter(user=request.user):
            userInfo = UserInfo.objects.get(user=request.user)
        else:
            userInfo = UserInfo.objects.create(
                user = request.user,
            )
        
        try:
            orig = request.FILES['image'].read()
            image = Image.open(StringIO(orig))
        except IOError:
            return HttpResponse(json.dumps({'error': 'Sorry, there is a problem with the file.'}))
        
        
        (w, h) = image.size
            
        top = float(topPercent)*h
        left = float(leftPercent)*w
        right = float(rightPercent)*w
        bottom = float(bottomPercent)*h
        box = [ int(left), int(top), int(right), int(bottom) ]
        
        
        
        image = image.crop(box)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image = image.resize((150, 150), Image.ANTIALIAS)
            
        fullPath = os.path.join(ROOT_PATH, path)
        image.save(fullPath, 'JPEG', quality=90)
        
        userInfo.avatar = "/"+path
        userInfo.save()
        srcLink = path
        
        
            
    else:
        srcLink = False
    

    
    return HttpResponse(json.dumps({'src': srcLink}))






@login_required
def backgroundImageCrop(request):
    if request.method == 'POST':
        imageFile = request.FILES["image"]
        topPercent = request.POST["topPercent"]
        leftPercent = request.POST["leftPercent"]
        bottomPercent = request.POST["bottomPercent"]
        rightPercent = request.POST["rightPercent"]
        
        path = avatarFilePath(user=request.user, 
            filename=request.FILES['image'].name, avatarName='backgroundImageLarge.jpg')
        
        
        if UserInfo.objects.filter(user=request.user):
            userInfo = UserInfo.objects.get(user=request.user)
        else:
            userInfo = UserInfo.objects.create(
                user = request.user,
            )
        
        try:
            orig = request.FILES['image'].read()
            image = Image.open(StringIO(orig))
        except IOError:
            return HttpResponse(json.dumps({'error': 'Sorry, there is a problem with the file.'}))
        
        
        (w, h) = image.size
            
        top = float(topPercent)*h
        left = float(leftPercent)*w
        right = float(rightPercent)*w
        bottom = float(bottomPercent)*h
        box = [ int(left), int(top), int(right), int(bottom) ]
        
        
        
        image = image.crop(box)
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        #make the large background image
        image = image.resize((1500, 500), Image.ANTIALIAS)
            
        fullPath = os.path.join(ROOT_PATH, path)
        image.save(fullPath, 'JPEG', quality=100)
        
        userInfo.backgroundImageLarge = "/"+path
        largePath = path
        
        #make the small background image
        image = image.resize((600, 200), Image.ANTIALIAS)
        
        head, tail = os.path.split(path)
        fullPath = os.path.join(ROOT_PATH, head, "backgroundImageSmall.jpg")
        image.save(fullPath, 'JPEG', quality=90)
        
        userInfo.backgroundImageSmall = "/"+os.path.join(head,"backgroundImageSmall.jpg")
        
        
        userInfo.save()
        srcLink = largePath
        
        
            
    else:
        srcLink = False
    

    
    return HttpResponse(json.dumps({'src': srcLink}))
















































#-------------------- Misc Functions -------------------------------------------------


def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise






