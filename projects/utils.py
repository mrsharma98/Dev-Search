from .models import Project, Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateProjects(request, projects, resultsPerPage):

  page = request.GET.get('page')
  resultsPerPage = resultsPerPage
  paginator = Paginator(projects, resultsPerPage)

  try:
    projects = paginator.page(page)
  except PageNotAnInteger:
    # if there is no page in url
    page = 1
    projects = paginator.page(page)
  except EmptyPage:
    # if page number exceeds like if user write page=10000 in url and we don't have it
    page = paginator.num_pages
    # this gives the last page
    projects = paginator.page(page)

  # if we have n pages, we will show 3 at a time
  leftIndex = (int(page) - 1)
  if leftIndex < 1:
    leftIndex = 1

  rightIndex = (int(page) + 2)
  if rightIndex > paginator.num_pages:
    rightIndex = paginator.num_pages + 1
 
  custom_range = range(leftIndex, rightIndex)

  return custom_range, projects


def searchProjects(request):
  search_query = ''

  if request.GET.get('search_query'):
    search_query = request.GET.get('search_query')

  tags = Tag.objects.filter(name__icontains=search_query)

  projects = Project.objects.distinct().filter(
    Q(title__icontains=search_query) |
    Q(description__icontains=search_query) |
    Q(owner__name__icontains=search_query) |
    Q(tags__in=tags)
  )

  return projects, search_query
