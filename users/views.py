from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User

# Create your views here.

def profiles(request):
  profiles = Profile.objects.all()
  context = {'profiles': profiles}
  return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
  profile = Profile.objects.get(id=pk)

  # skills with description
  topSkills = profile.skill_set.exclude(description__exact="")
  # exclude if skill does not have a decription.

  # Skills with no description
  otherSkills = profile.skill_set.filter(description__exact="")

  context = {'profile': profile, 'topSkills': topSkills, 'otherSkills': otherSkills}
  return render(request, 'users/user-profile.html', context)


def loginPage(request):

  if request.user.is_authenticated:
    return redirect('profiles')

  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    try:
      user = User.objects.get(username=username)
    except:
      print('Username does not exist')
      messages.error(request, 'Username does not exist')

    user = authenticate(request, username=username, password=password)
    # this takes request, username and password -- returns either user instance or None

    if user is not None:
      login(request, user)
      # this creates a session for the user in the db
      # also it stores the session into our browser cookies.
      return redirect('profiles')
    else:
      print('Username or password is incorrect')
      messages.error(request, 'Username or password is incorrect')

  return render(request, 'users/login_register.html')


def logoutUser(request):
  # logout -- takes request and user -- deletes the session from the cookie
  logout(request)
  messages.error(request, 'User was logged oSut!')
  return redirect('login')