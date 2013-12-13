from django.db import models
from django.contrib.auth.models import User

# Create your models here.

CHANGE_PRIORITY = (
						('1', '1'),
						('2', '2'),
						('3', '3'),
						('4', '4'),
						('5', '5'),
)

CHANGE_STATUS = (
						('In Preparation', 'In Preparation'),
						('Submitted', 'Submitted'),
						('Accepted', 'Accepted'),
						('Rejected', 'Rejected'),
						('Completed', 'Completed'),
)

class RequestForChange(models.Model):

	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)
	priority = models.CharField(max_length=255, choices=CHANGE_PRIORITY)
	status = models.CharField(max_length=255, choices=CHANGE_STATUS)
	date_resolved = models.DateTimeField(blank=True, null=True)
	resolution = models.TextField(max_length=10240, blank=True)
	approver = models.ForeignKey(User, related_name='rfc_approver', blank=True, null=True)
	requestor = models.ForeignKey(User, related_name='rfc_requestor')
	approval_comments = models.TextField(max_length=1024, blank=True)
	change_description = models.TextField(max_length=10240)

	def __str__(self):
		return '''%s %s''' % ( self.requestor, self.created_date )
	
