from django.shortcuts import render
from .models import Profile
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