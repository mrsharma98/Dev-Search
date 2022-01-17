from multiprocessing import context
from django.shortcuts import render
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
  context = {'form': form}
  return render(request, 'projects/project_form.html', context)