from .models import Profile, Skill
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateProfiles(request, profiles, resultsPerPage):

  page = request.GET.get('page')
  resultsPerPage = resultsPerPage
  paginator = Paginator(profiles, resultsPerPage)

  try:
    profiles = paginator.page(page)
  except PageNotAnInteger:
    # if there is no page in url
    page = 1
    profiles = paginator.page(page)
  except EmptyPage:
    # if page number exceeds like if user write page=10000 in url and we don't have it
    page = paginator.num_pages
    # this gives the last page
    profiles = paginator.page(page)

  # if we have n pages, we will show 3 at a time
  leftIndex = (int(page) - 1)
  if leftIndex < 1:
    leftIndex = 1

  rightIndex = (int(page) + 2)
  if rightIndex > paginator.num_pages:
    rightIndex = paginator.num_pages + 1
 
  custom_range = range(leftIndex, rightIndex)

  return custom_range, profiles



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