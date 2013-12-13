from django import template
from wbs.models import WorkItem, EngineeringDay
from wbs.forms import WBSForm, EngineeringDayForm

register = template.Library()


def get_wbs_form(wbs):

	try:
		r = WorkItem.objects.get(id=wbs)
	except WorkItem.DoesNotExist:
		return ''
	f = WBSForm(r.project.all()[0], instance=r)
	return f.as_table()
register.simple_tag(get_wbs_form)

def get_engineering_day_form(wbs):
	
	form = EngineeringDayForm()
	form.auto_id = "id_engineering_day_%s" % wbs.id + "_%s"
	return form.as_table()
register.simple_tag(get_engineering_day_form)
