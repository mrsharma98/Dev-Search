import imp
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Project
from .forms import ProjectForm
from .utils import searchProjects, paginateProjects

# Create your views here.

def projects(request):

  projects, search_query = searchProjects(request)
  custom_range, projects = paginateProjects(request, projects, 6)
  
  
  context = {'projects': projects, 'search_query': search_query, 'custom_range':custom_range}
  return render(request, 'projects/projects.html', context)


def project(request, pk):
  projectObj = Project.objects.get(id=pk)
  # tags = projectObj.tags.all()
  context = {'project': projectObj}
  return render(request, 'projects/single-project.html', context)


# sending the user to the login page if they are not logged in
@login_required(login_url="login")
def createProject(request):
  profile = request.user.profile
  form = ProjectForm()
  # this is for parsing in the context

  if request.method == 'POST':
    # if req is post -- then process the form
    # print(request.POST) -- to get the form POST data
    # gives a dictionary
    form = ProjectForm(request.POST, request.FILES)
    if form.is_valid():
      project = form.save(commit=False)
      project.owner = profile
      project.save()
      return redirect('account') # -- projects -- url name

  context = {'form': form}
  return render(request, 'projects/project_form.html', context)


@login_required(login_url="login")
def updateProject(request, pk):
  profile = request.user.profile
  project = profile.project_set.get(id=pk)
  # this makes sure that only the owner can update the project

  form = ProjectForm(instance=project)
  # by passing the instance will prefill all the project data

  if request.method == 'POST':
    form = ProjectForm(request.POST, request.FILES, instance=project)
    # with data, we need to tell what instance/obj we are updating, so sending the project
    if form.is_valid():
      form.save()
      return redirect('account') # -- projects -- url name

  context = {'form': form}
  return render(request, 'projects/project_form.html', context)


@login_required(login_url="login")
def deleteProject(request, pk):
  profile = request.user.profile
  project = profile.project_set.get(id=pk)

  if request.method == 'POST':
    project.delete()
    return redirect('account')
  
  context = {'object': project}
  return render(request, 'delete_template.html', context)