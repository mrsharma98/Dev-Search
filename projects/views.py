from django.shortcuts import render, redirect
from .models import Project
from .forms import ProjectForm

# Create your views here.

def projects(request):
  projects = Project.objects.all()
  context = {'projects': projects}
  return render(request, 'projects/projects.html', context)


def project(request, pk):
  projectObj = Project.objects.get(id=pk)
  # tags = projectObj.tags.all()
  context = {'project': projectObj}
  return render(request, 'projects/single-project.html', context)


def createProject(request):

  form = ProjectForm()
  # this is for parsing in the context

  if request.method == 'POST':
    # if req is post -- then process the form
    # print(request.POST) -- to get the form POST data
    # gives a dictionary
    form = ProjectForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      return redirect('projects') # -- projects -- url name

  context = {'form': form}
  return render(request, 'projects/project_form.html', context)


def updateProject(request, pk):
  project = Project.objects.get(id=pk)
  form = ProjectForm(instance=project)
  # by passing the instance will prefill all the project data

  if request.method == 'POST':
    form = ProjectForm(request.POST, request.FILES, instance=project)
    # with data, we need to tell what instance/obj we are updating, so sending the project
    if form.is_valid():
      form.save()
      return redirect('projects') # -- projects -- url name

  context = {'form': form}
  return render(request, 'projects/project_form.html', context)


def deleteProject(request, pk):
  project = Project.objects.get(id=pk)
  context = {'object': project}

  if request.method == 'POST':
    project.delete()
    return redirect('projects')

  return render(request, 'projects/delete_template.html', context)