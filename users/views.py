from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, ProfileForm, SkillForm
from .utils import searchProfiles, paginateProfiles


# Create your views here.

def profiles(request):
  profiles, search_query = searchProfiles(request)

  custom_range, profiles = paginateProfiles(request, profiles, 6)

  context = {'profiles': profiles, 'search_query': search_query, 'custom_range': custom_range}
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


def loginUser(request):
  page = 'login'

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
  messages.info(request, 'User was logged out')
  return redirect('login')


def registerUser(request):
  page = 'register'

  if request.user.is_authenticated:
    return redirect('profiles')

  form = CustomUserCreationForm()
  
  if request.method == 'POST':
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      # it will just give us the instance without saving it to the db

      user.username = user.username.lower()
      user.save()
      
      messages.success(request, 'User account was created.')
      
      login(request, user)
      return redirect('edit-account')
    
    else:
      messages.error(request, 'An error has occured during registration')


  context = {'page': page, 'form': form}

  return render(request, 'users/login_register.html', context)


@login_required(login_url='login')
def userAccount(request):
  # getting logged in user
  profile = request.user.profile
  skills = profile.skill_set.all()
  projects = profile.project_set.all()

  context = {'profile': profile, 'skills': skills, 'projects': projects}

  return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
  profile = request.user.profile
  form = ProfileForm(instance=profile)

  if request.method == 'POST':
    form = ProfileForm(request.POST, request.FILES, instance=profile)

    # updaing profile -- and signal is taking care of user related updated field data.
    if form.is_valid():
      form.save()
      return redirect('account')

  context = {'form': form}
  return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def createSkill(request):
  profile = request.user.profile
  form = SkillForm()

  if request.method == 'POST':
    form = SkillForm(request.POST)

    if form.is_valid():
      skill = form.save(commit=False)
      skill.owner = profile
      skill.save()
      messages.success(request, 'Skill was added successfully!')
      return redirect('account')

  context = {'form': form}
  return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def updateSkill(request, pk):
  profile = request.user.profile
  skill = profile.skill_set.get(id=pk)
  form = SkillForm(instance=skill)

  if request.method == 'POST':
    form = SkillForm(request.POST, instance=skill)

    if form.is_valid():
      form.save()
      messages.success(request, 'Skill was updated successfully!')
      return redirect('account')

  context = {'form': form}
  return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def deleteSkill(request, pk):
  profile = request.user.profile
  skill = profile.skill_set.get(id=pk)

  if request.method == 'POST':
    skill.delete()
    messages.success(request, 'Skill was deleted successfully!')
    return redirect('account')
  
  context = {'object': skill}

  return render(request, 'delete_template.html', context)