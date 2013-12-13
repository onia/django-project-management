from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.html import linebreaks

# Create your models here.

class Issue(models.Model):

    ISSUE_TYPE = (
        (1, 'Request For Change'),
        (2, 'Off Specifications'),
        (3, 'Concern'),
        (4, 'Question'),
    )

    ISSUE_STATUS = (
        (1, 'Open'),
        (2, 'In Progress'),
        (3, 'Completed'),
        (4, 'Closed'),
    )

    ISSUE_PRIORITY = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    description = models.TextField('Description', max_length=10240)
    owner = models.ForeignKey(User, related_name='owned_issued', verbose_name='Owner')
    author = models.ForeignKey(User, related_name='issued_authored', verbose_name='Author')
    type = models.IntegerField(choices=ISSUE_TYPE, verbose_name='Type')
    status = models.IntegerField(choices=ISSUE_STATUS, verbose_name='Status')
    priority = models.IntegerField(choices=ISSUE_PRIORITY, verbose_name='Priority')
    related_rfc = models.CharField(max_length=1024, blank=True, verbose_name='Related RFC')
    related_helpdesk = models.CharField(max_length=1024, blank=True, verbose_name='Related Helpdesk')
    history = models.TextField('History', blank=True)       

    def __str__(self):
        return self.description[:50]    

    def get_history_html(self):
        return linebreaks(self.history)

        
