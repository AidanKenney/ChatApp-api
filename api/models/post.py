from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Post(models.Model):
  # define fields
  # https://docs.djangoproject.com/en/3.0/ref/models/fields/
  title = models.CharField(max_length=100)
  content = models.CharField(max_length=200)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  owner = models.ForeignKey(
      get_user_model(),
      related_name='posts',
      on_delete=models.CASCADE
  )

  def __str__(self):
    # This must return a string
    return f"The post by '{self.owner}' is titled {self.title}: {self.content}."

  def as_dict(self):
    """Returns dictionary version of Post models"""
    return {
        'id': self.id,
        'title': self.title,
        'content': self.content,
        'owner': self.owner
    }
