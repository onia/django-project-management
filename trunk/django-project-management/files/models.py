from django.db import models
from django.contrib.auth.models import User
import settings
import os
import time

# Create your models here.

FILE_TYPE = (
                                (1, 'Project Plan'),
                                (2, 'Other File'),
)


class ProjectFile(models.Model):

        author = models.ForeignKey(User, related_name='file_author')
        file_type = models.IntegerField(choices=FILE_TYPE)
        description = models.TextField(max_length=1024)
        created_date = models.DateTimeField(auto_now_add=True)
        filename = models.FileField(upload_to="uploaded_files/%Y/%m/%d")
        
        def __str__(self):
                return '''%s''' % self.id

        def get_absolute_url(self):
                return '''/files/%s''' % self.filename
