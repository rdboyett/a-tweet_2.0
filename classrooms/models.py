import datetime

from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models




class ConversationMessage(models.Model):
    text = models.TextField(max_length=150)
    timeDate = models.DateTimeField(auto_now=True)
    favorites = models.IntegerField(default=0, blank=True, null=True)
    
    
    def __unicode__(self):
      return u'%s' % (self.text)




class Message(models.Model):
    text = models.TextField(max_length=150)
    timeDate = models.DateTimeField(auto_now=True)
    retweets = models.IntegerField(default=0, blank=True, null=True)
    favorites = models.IntegerField(default=0, blank=True, null=True)
    ConversationMessages = models.ManyToManyField(ConversationMessage, blank=True, null=True)
    isRetweet = models.BooleanField(default=False)
    originalUser = models.ForeignKey(User, blank=True, null=True)
    
    
    def __unicode__(self):
      return u'%s' % (self.text)
    
    
    class Meta:
        ordering = ['-timeDate']
    

class HashTag(models.Model):
    tag = models.CharField(max_length=45)
    timeDate = models.DateTimeField(auto_now=True)
    messages = models.ManyToManyField(Message, blank=True, null=True)
    classroomID = models.IntegerField()
    
    
    def __unicode__(self):
      return u'%s' % (self.tag)


class Trending(models.Model):
    school = models.CharField(max_length=45, blank=True, null=True)
    hashtag1 = models.CharField(max_length=45, blank=True, null=True)
    hashtag2 = models.CharField(max_length=45, blank=True, null=True)
    hashtag3 = models.CharField(max_length=45, blank=True, null=True)
    hashtag4 = models.CharField(max_length=45, blank=True, null=True)
    hashtag5 = models.CharField(max_length=45, blank=True, null=True)
    hashtag6 = models.CharField(max_length=45, blank=True, null=True)
    hashtag7 = models.CharField(max_length=45, blank=True, null=True)
    hashtag8 = models.CharField(max_length=45, blank=True, null=True)
    hashtag9 = models.CharField(max_length=45, blank=True, null=True)
    hashtag10 = models.CharField(max_length=45, blank=True, null=True)
    timeDate = models.DateTimeField(auto_now=True)

    def __unicode__(self):
      return u'%s' % (self.school)
    
    
    
    
class PublicMessage(models.Model):
    school = models.CharField(max_length=45)
    messages = models.ManyToManyField(Message, blank=True, null=True)


    def __unicode__(self):
      return u'%s' % (self.school)
    
    
    
    
    
class Classroom(models.Model):
    name = models.CharField(max_length=45)
    code = models.CharField(max_length=10)
    messages = models.ManyToManyField(Message, blank=True, null=True)
    allowJoin = models.BooleanField(default=True)
    classOwnerID = models.IntegerField()


    def __unicode__(self):
      return u'%s' % (self.name)


class Following(models.Model):
    user = models.ForeignKey(User)


    def __unicode__(self):
      return u'%s %s' % (self.user.last_name, self.user.first_name)



class ClassUser(models.Model):
    user = models.ForeignKey(User)
    school = models.CharField(max_length=45, blank=True, null=True)
    teacher = models.BooleanField(default=True)
    readOnly = models.BooleanField(default=False)
    messages = models.ManyToManyField(Message, blank=True, null=True)
    classrooms = models.ManyToManyField(Classroom, blank=True, null=True)
    avatarBackColor = models.CharField(max_length=45, blank=True, null=True)
    avatarTextColor = models.CharField(max_length=45, blank=True, null=True)


    def __unicode__(self):
      return u'%s' % (self.user)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
