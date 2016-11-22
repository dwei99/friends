from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from models import User,Friendships
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import bcrypt


# Create your views here.
def index(request):
    if 'user_id' not in request.session:
        request.session['user_id'] = 0
    return render (request,"friends_app/main.html")
def register(request):
    if request.method == 'POST':
        try:
            validate_email(request.POST['email'])
        except ValidationError as e:
            messages.add_message(request,messages.ERROR, 'Please enter a valid email')
        else:
            password = request.POST['password']
            hashed = bcrypt.hashpw(password.encode(),bcrypt.gensalt())
        if len(request.POST['password']) < 8:
            messages.add_message(request,messages.ERROR, 'Please enter a password of 8 characters or more')
        else:
            if len(request.POST['name']) < 3:
                    messages.add_message(request,messages.ERROR, 'Please enter a name of 3 characters or more')

            user = User.objects.create(name=request.POST['name'],email=request.POST['email'],password=hashed, alias=request.POST['alias'], dob=request.POST['dob'])
            messages.add_message(request,messages.INFO, 'You have successfully registered')

    return redirect('/')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if len(request.POST['password']) < 8:
            messages.add_message(request,messages.ERROR, 'Please enter a password or 8 or more characters')
        else:
            try:
                user = User.objects.get(email=email)
            except:
                messages.add_message(request,messages.ERROR, "User doesn't exist")
                return redirect('/')
            else:
                encoded_ps = bcrypt.hashpw(password.encode(), user.password.encode())
                print encoded_ps
                if encoded_ps != user.password.encode():
                    messages.add_message(request,messages.ERROR, "Password doesnt match for this user")
                    return redirect('/')
                else:
                    User.objects.login(email, encoded_ps)
                    if not user:
                        messages.add_message(request,messages.ERROR, "invalid login information")
                        return redirect('/')
                    if user:
                        #storing value in session to use for other features
                        request.session['userid'] = user.id
                        request.session['alias'] = user.alias
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
