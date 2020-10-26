from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Chat(models.Model):
  # define fields
  # https://docs.djangoproject.com/en/3.0/ref/models/fields/
  content = models.CharField(max_length=200)
  owner = models.ForeignKey(
      get_user_model(),
      on_delete=models.CASCADE
  )

  def __str__(self):
    # This must return a string
    return f"The chat by '{self.owner}' is {self.content}."

  def as_dict(self):
    """Returns dictionary version of Chat models"""
    return {
        'id': self.id,
        'content': self.content,
        'owner': self.owner
    }
