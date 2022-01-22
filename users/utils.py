from .models import Profile, Skill
from django.db.models import Q



def searchProfiles(request):

  search_query = ''

  if request.GET.get('search_query'):
    search_query = request.GET.get('search_query')
  
  skills = Skill.objects.filter(name__icontains=search_query)


  # here if w edon't use "Q()" (known as Q-lookup filter) then query will have to make in all aspect
  # and we use and &/| for multiple stuffs
  profiles = Profile.objects.distinct().filter(
    Q(name__icontains=search_query) | 
    Q(short_intro__icontains=search_query) |
    Q(skill__in=skills)
  )
  # as skills are added, it will give multiple profile for single user, as they have multiple skills
  # so distinct() solves the problem

  return profiles, search_query