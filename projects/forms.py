from dataclasses import fields
from tkinter import Widget
from django.forms import ModelForm
from django import forms
from .models import Project


class ProjectForm(ModelForm):
  class Meta:
    model = Project
    fields = ['title', 'featured_image', 'description', 'demo_link', 'source_link', 'tags']

    # makes tags option as checkbox
    widgets = {
      'tags': forms.CheckboxSelectMultiple()
    }

  def __init__(self, *args, **kwargs):
    super(ProjectForm, self).__init__(*args, **kwargs)

    # Method 1
    # selecting fields we want to modify (basically for adding css classes)
    # self.fields['title'].widget.attrs.update({'class': 'input', 'placeholder':'Add title'})
    # we are selecting the title in the form and adding a css class named input etc etc

    # self.fields['description'].widget.attrs.update({'class': 'input', 'placeholder':'Add description'})

    # Method 2 (usign for loop)
    for name, field in self.fields.items():
      # name -- key or label of the field
      # field -- value or field
      placeholder = 'Add '+name
      field.widget.attrs.update({'class': 'input', 'placeholder': placeholder})