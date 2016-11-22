from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from models import User,Friendships
from django.contrib import messages
import bcrypt


# Create your views here.
def index(request):
    if 'user_id' not in request.session:
        request.session['user_id'] = 0
    return render (request,"friends_app/main.html")

def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        alias = request.POST['alias']
        email = request.POST['email']
        password = request.POST['password']
        confirm_ps = request.POST['valpassword']
        dob = request.POST['dob']
        user = User.objects.register(request,name,alias,email,password,confirm_ps,dob)
        if not user:
            messages.add_message(request,messages.ERROR, 'Registration Failed')
            return redirect ('/')
        if user:
            messages.add_message(request,messages.INFO, 'You have successfully registered')
            return redirect ('/')
    return redirect('/')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.login(request,email,password)
        if not user:
            messages.add_message(request,messages.ERROR, "invalid login information")
            return redirect ('/')
        if user:
            return redirect ('/friends')
    return redirect ('/')

def friends(request):
    if 'user_id' not in request.session:
        request.session['user_id'] = 0
        messages.add_message(request,messages.warning, "Please login to continue")
        return redirect ('/')
    else:
        #Getting all user friends and non friends
        user_id = request.session['userid']
        your_friends = Friendships.objects.filter(user__id=user_id)
        print your_friends
        non_friends = User.objects.exclude(id = user_id).exclude(friendsfriend__in = Friendships.objects.exclude(friend = user_id))
        print non_friends
        context = {
                'your_friends': your_friends,
                'non_friends': non_friends
        }
        # print context
        return render (request, 'friends_app/friends.html', context)

def add_friend(request,id):
    user_id = request.session['userid']
    friend_id = id
    already_friends = Friendships.objects.filter(user= user_id).filter(friend = friend_id)
    if not already_friends:
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
    del request.session['userid']
    return redirect ('/')
