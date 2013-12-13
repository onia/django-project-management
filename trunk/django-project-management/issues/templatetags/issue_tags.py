from django import template
from issues.models import Issue
from issues.forms import IssueForm

register = template.Library()


def get_issue_form(issue):

	try:
		r = Issue.objects.get(id=issue)
	except Issue.DoesNotExist:
		return ''
	f = IssueForm(instance=r)
	return f.as_table()

register.simple_tag(get_issue_form)
	
