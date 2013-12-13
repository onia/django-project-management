from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Deliverable(models.Model):

        description = models.TextField('Description', max_length=10240)
        acceptance_criteria = models.TextField('Acceptance Criteria', max_length=10240)
        deliverable_tester = models.CharField('Deliverable Tester', max_length=255)
        testing_method = models.TextField('Method', max_length=10240)
        expected_result = models.TextField('Expected Result', max_length=10240)
        rpo = models.CharField('Recovery Point Objective', max_length=255, blank=True)
        rto = models.CharField('Recovery Time Objective', max_length=255, blank=True)
        created_date = models.DateTimeField(auto_now_add=True)
        modified_date = models.DateTimeField(auto_now=True)

        def __str__(self):
                return self.description
