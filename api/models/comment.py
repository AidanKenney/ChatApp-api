from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Comment(models.Model):
  # define fields
  # https://docs.djangoproject.com/en/3.0/ref/models/fields/
  content = models.CharField(max_length=200)
  owner = models.ForeignKey(
      get_user_model(),
      related_name='comments',
      on_delete=models.CASCADE
  )
  post = models.ForeignKey(
      'Post',
      related_name='comments',
      on_delete=models.CASCADE
  )

  def __str__(self):
    # This must return a string
    return f"The comment is by '{self.owner}': {self.content}."

  def as_dict(self):
    """Returns dictionary version of Comment models"""
    return {
        'id': self.id,
        'content': self.content,
        'owner': self.owner
    }
