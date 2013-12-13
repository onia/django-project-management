from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class LessonLearnt(models.Model):

        author = models.ForeignKey(User)
        description = models.TextField(max_length=10240)
        created_date = models.DateTimeField(auto_now_add=True)
        modified_date = models.DateTimeField(auto_now=True)
        publish_to_client = models.BooleanField(default=False)

        def __str__(self):
                return self.description
