from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile



# This are receivers


# sender - the model who send this
# instance - the instance of the model who triggered this signal.
# created (true or false) - it says if a new user/item created into the db or not
# @receiver(post_save, sender=Profile)
def createProfile(sender, instance, created, **kwargs):
  # anytime a user model is created we will create a profile for the same
  if created:
    user = instance

    # these parameters will be assigned to the Profile
    profile = Profile.objects.create(
      user = user,
      username = user.username,
      email = user.email,
      name = user.first_name
    )
    

# when we deleted user, the profile gets deleted automatically bcz of relation we have in Profile model
# but when profile is deleted, user stays-- so here we will take care of it
def deleteUser(sender, instance, **kwargs):
  user = instance.user
  user.delete()


# we can use decorators instead of connecting like this
post_save.connect(createProfile, sender=User)
post_delete.connect(deleteUser, sender=Profile)