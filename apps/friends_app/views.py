from django.shortcuts import render,redirect,HttpResponse
from models import User,Friendships
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import bcrypt


# Create your views here.
def index(request):
    return render (request,"friends_app/main.html")
def register(request):
    if request.method == 'POST':
        try:
            validate_email(request.POST['email'])
        except ValidationError as e:
            messages.add_message(request,messages.ERROR, 'Please enter a valid email')
        else:
            password = request.POST['password']
            #hashed = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
            user = User.objects.create(name=request.POST['name'],email=request.POST['email'],password=password, alias=request.POST['alias'], dob=request.POST['dob'])
        if len(request.POST['password']) < 8:
            messages.add_message(request,messages.ERROR, 'Please enter a password of 8 characters or more')
    return redirect('/')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        #hashed = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        # unhashed = bcrypt.hashpw(password.encode('utf-8'), hashed)
        user = User.objects.login(email, password)
        if user == False:
            return redirect('/')
        if user == True:
            user_info = User.objects.get(email = email,password = password)
            #storing value in session to use for other features
            request.session['userid'] = user_info.id
            request.session['alias'] = user_info.alias
            return redirect ('/friends')

def friends(request):
    #Getting all user friends and non friends
    user_id = request.session['userid']
    all_friends = Friendships.objects.all()
    your_friends = all_friends.select_related("friend").filter(user__id=user_id)
    #non_friends = all_friends.select_related("user").exclude(user__id=user_id)
    non_friends = all_friends.raw('select a.id, a.alias from friends_app_user a left join friends_app_friendships b on b.friend_id != a.id WHERE a.id  !=%s;',[user_id])
    print non_friends
    request.session['message'] = 'You have no friends yet'
    context = {
            'your_friends': your_friends,
            'non_friends': non_friends,
    }
    # print context
    return render (request, 'friends_app/friends.html', context)

def add_friend(request,id):
        user_id = request.session['userid']
        friendship = Friendships.objects.create(user_id= user_id, friend_id=id)
        return redirect ('/friends')

def user(request,id):
    user_profile = User.objects.filter(id = id)
    context = {
            'user_profile': user_profile
    }
    return render (request, 'friends_app/user.html',context)

def end(request, id):
    user_id = request.session['userid']
    remove_friend = Friendships.objects.get(friend_id = id,user_id = user_id).delete()
    return redirect ('/friends')


def logout(request):
    request.session['userid'] = 0
    return redirect ('/')
