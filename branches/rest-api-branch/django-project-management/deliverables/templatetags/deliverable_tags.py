from django import template
from deliverables.models import Deliverable
from deliverables.forms import DeliverableForm

register = template.Library()


def get_deliverable_form(deliverable):

	try:
		d = Deliverable.objects.get(id=deliverable)
	except Deliverable.DoesNotExist:
		return ''
	f = DeliverableForm(instance=d)
	return f.as_table()

register.simple_tag(get_deliverable_form)
	
