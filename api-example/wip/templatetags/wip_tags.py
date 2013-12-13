from django import template
from django.contrib.auth.models import User, Group
from wip.models import Heading
from wip.forms import WIPHeadingForm, WIPItemEditorForm

register = template.Library()


def get_heading_form():
	f = WIPHeadingForm()
	return f.as_table()
register.simple_tag(get_heading_form)
	
def get_work_item_form(wip_report):
	f = WIPItemEditorForm(wip_report)
	return f.as_table()
register.simple_tag(get_work_item_form)

def get_css_for_permissions(user, wip_report):
	allow_access = None
	for group in user.groups.all():
		if group in wip_report.write_acl.all():
			allow_access = True

	if allow_access:
		return '''display: inline;'''
	else:
		return '''display: none;'''
register.simple_tag(get_css_for_permissions)
		

	

	
