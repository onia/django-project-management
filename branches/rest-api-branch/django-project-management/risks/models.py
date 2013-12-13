from django.db import models
from django.contrib.auth.models import User
from django.utils.html import linebreaks
# Create your models here.

class Risk(models.Model):

    RISK_PROBABILITY_IMPACT = (     
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    RISK_COUNTER_MEASURE = ( 
        (1, 'Prevention'),
        (2, 'Acceptance'),
        (3, 'Transfer'),
        (4, 'Reduction'),
        (5, 'Contingency'),
    )

    RISK_STATUS = ( 
        (1, 'Closed'),
        (2, 'Reducing'),
        (3, 'Increasing'),
        (4, 'No Change'),
    )

    risk_number = models.CharField(max_length=255, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    description = models.TextField(max_length=10240)
    owner = models.ForeignKey(User, related_name='risk_owner')
    probability = models.IntegerField(choices=RISK_PROBABILITY_IMPACT)
    impact = models.IntegerField(choices=RISK_PROBABILITY_IMPACT)
    rating = models.IntegerField(null=True, blank=True)
    counter_measure = models.IntegerField(choices=RISK_COUNTER_MEASURE)
    status = models.IntegerField(choices=RISK_STATUS)
    history = models.TextField('History', blank=True)       

    def __str__(self):
        return self.risk_number

    def get_absolute_url(self):
        return '''/Risks/%s''' % self.risk_number
    
    def get_history_html(self):
        return linebreaks(self.history)
