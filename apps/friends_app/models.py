from __future__ import unicode_literals
from django.contrib import messages
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import bcrypt


# Create your models here.
class UserManager(models.Manager):
    def register(self,request,name,alias,email,password,confirm_ps,dob):
        if len(name) < 3:
            messages.add_message(request,messages.ERROR, 'Please enter a name of 3 characters or more')
        if len(alias) < 3:
            messages.add_message(request,messages.ERROR, 'Please enter a alias of 3 characters or more ')
        try:
            validate_email(email)
        except ValidationError as e:
            messages.add_message(request,messages.ERROR, 'Please enter a valid email')
        else:
            password_entered = password
            if len(password_entered) < 8:
                messages.add_message(request,messages.ERROR, 'Please enter a password of 8 characters or more')
            if password_entered != confirm_ps:
                messages.add_message(request,messages.ERROR, 'The password and confirm password do not match!')
            if len(dob) == 0:
                messages.add_message(request,messages.ERROR, 'Please enter a date of birth in mm/dd/yyyy format')
            else:
                hashed = bcrypt.hashpw(password_entered.encode(),bcrypt.gensalt())
                user = User.objects.create(name=name,alias=alias,email=email,password=hashed,dob=dob)
                if not user:
                    return False
                if user:
                    return True

    def login(self,request,email,password):
        try:
            user = User.objects.get(email=email)
        except:
            messages.add_message(request,messages.ERROR, "User doesn't exist")
            return False
        else:
            if len(password) < 8:
                messages.add_message(request,messages.ERROR, 'Please enter a password or 8 or more characters')
            else:
                encoded_ps = bcrypt.hashpw(password.encode(), user.password.encode())
                if encoded_ps != user.password.encode():
                    messages.add_message(request,messages.ERROR, "Password doesnt match for this user")
                    return False
                else:
                    #storing value in session to use for other features
                    request.session['userid'] = user.id
                    request.session['alias'] = user.alias
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
    email = models.CharField(max_length=255, unique = True)
    password = models.CharField(max_length=100)
    dob = models.DateField(auto_now_add=False)
    create_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateField(auto_now_add=True)
    objects = UserManager()

class Meta:
    managed = False
    db_table = 'users'
