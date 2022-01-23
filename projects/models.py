from ast import Num
from email.policy import default
from django.db import models
import uuid
from users.models import Profile

# Create your models here.

class Project(models.Model):
  owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
  # if user profile has deleted then owner value will set to null

  title = models.CharField(max_length=200)
  description = models.TextField(null=True, blank=True)
  # null --> this value can be null
  # blank --> when we submit the form, the form will accept it even if this field is blank
  demo_link = models.CharField(max_length=2000, null=True, blank=True)

  featured_image = models.ImageField(null=True, blank=True, default="default.jpg")

  source_link = models.CharField(max_length=2000, null=True, blank=True)
  tags = models.ManyToManyField('Tag', blank=True)
  # putting Tag in quotes as we have defined Tag model below and not above the Project model
  
  # we want to store the review value in project so -- 
  vote_total = models.IntegerField(default=0, null=True, blank=True)
  vote_ratio = models.IntegerField(default=0, null=True, blank=True)

  created = models.DateTimeField(auto_now_add=True)
  id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

  
  def __str__(self):
    return self.title


  class Meta:
    # ordering projects based on created date
    ordering = ['created']


class Review(models.Model):

  VOTE_TYPE = (
    ('up', 'Up Vote'),
    ('down', 'Down Vote'),
    # (database value, display or string representation)
  )

  # owner =
  project = models.ForeignKey(Project, on_delete=models.CASCADE)
  # ForeignKey establishs One to Many relationship
  body = models.TextField(null=True, blank=True)
  value = models.CharField(max_length=200, choices=VOTE_TYPE)
  created = models.DateTimeField(auto_now_add=True)
  id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)


  def __str__(self):
    return self.value



class Tag(models.Model):
  name = models.CharField(max_length=200)
  created = models.DateTimeField(auto_now_add=True)
  id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)


  def __str__(self):
    return self.name


# Query
# queryset = ModelName.objects.al()
# queryset -- Variable that holds response
# ModelName -- Model name
# objects -- Model objects attribute
# all() -- Method
# other methods(get(), filter(), exclude())
# get() -- gives single object based on the attribute
# filter() -- filters out based on the attributes
# exclude() -- excludes objects where the attributes condition meet
            # opposite of filter