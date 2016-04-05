
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User






class UserInfo(models.Model):
    user = models.ForeignKey(User)
    school = models.CharField(max_length=65, blank=True, null=True)
    teacher = models.BooleanField(default=False)
    title = models.CharField(max_length=3, blank=True, null=True)
    avatar = models.FilePathField(blank=True, null=True)
    backgroundImageSmall = models.FilePathField(blank=True, null=True)
    backgroundImageLarge = models.FilePathField(blank=True, null=True)


    def __unicode__(self):
      return u'%s' % (self.user)
    

        

admin.site.register(UserInfo)
      



