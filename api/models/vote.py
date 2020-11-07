from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Vote(models.Model):
  # define fields
  # https://docs.djangoproject.com/en/3.0/ref/models/fields/
  up_or_down = models.BooleanField(default=None)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  owner = models.ForeignKey(
      get_user_model(),
      related_name='votes',
      on_delete=models.CASCADE
  )
  post = models.ForeignKey(
      'Post',
      related_name='votes',
      on_delete=models.CASCADE
  )

  def __str__(self):
    # This must return a string
    return f"The vote is by '{self.owner}'  belongs on {self.post}."

  def as_dict(self):
    """Returns dictionary version of Vote models"""
    return {
        'id': self.id,
        'post': self.post,
        'owner': self.owner
    }
