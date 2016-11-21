from __future__ import unicode_literals

from django.db import models

# Create your models here.
class UserManager(models.Manager):
    def login(self, email, password):
        #search for user record if there is a match return user, if not return none
        user = User.objects.filter(email = email).filter(password = password)
        print user
        if not user:
            print "fail"
            return False
        else:
            print "true"
            return True

class Friendships(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, related_name="usersfriend")
    friend = models.ForeignKey('User', models.DO_NOTHING, related_name ="friendsfriend")
    create_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateField(auto_now_add=True)

class Meta:
    managed = False
    db_table = 'friendships'

class User(models.Model):
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=50)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=100)
    dob = models.DateField(auto_now_add=False)
    create_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateField(auto_now_add=True)
    objects = UserManager()

class Meta:
    managed = False
    db_table = 'users'
