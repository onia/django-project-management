from django import template
from rota.models import RotaItem
from rota.forms import RotaItemForm
from wbs.models import EngineeringDay

register = template.Library()


def get_activity_for_day(user, day):
	try:
		r = RotaItem.objects.get(date=day, person=user)
	except RotaItem.DoesNotExist:
		return '--'
	return r.activity
register.simple_tag(get_activity_for_day)


def get_project_task_for_day(user, day):

	''' Get and display the engineering days for this day, for this resource.
		An engineering day is a half-days work, and so one resource might be booked on 2 engineering days on one day. An 
		engineering day might be linked to a WorkItem or a WIPItem '''

	r = EngineeringDay.objects.filter(work_date=day, resource=user)
	print r

	if len(r) == 0:
		return '&nbsp;' 	# Easy enough, this resource has no engineering days assigned to him
	
	if len(r) == 1:	# If the user has an entire day assigned to this task
		if len(r[0].work_item.all()) != 0:
			str = '''<b>%s</b><br><a href="%s">%s</a><br>%s''' % ( r[0].work_item.all()[0].project.all()[0].project_number, r[0].get_absolute_url(), r[0].work_item.all()[0].title, r[0].get_day_type_display() )
			return str
		elif len(r[0].wip_item.all()) != 0:
			#str = '''<b>%s</b><br><a href="%s">%s</a><br>%s''' % ( r[0].work_item.all()[0].heading.all()[0], r[0].get_absolute_url(), r[0].work_item.all()[0].description, r[0].get_day_type_display() )
			str = '''<b>WIP Item</b><br><a href="%s">%s</a><br>%s''' % ( r[0].wip_item.all()[0].get_absolute_url(), r[0].wip_item.all()[0], r[0].get_day_type_display() )
			return str

	if len(r) == 2:		# If the user has 2 seperate tasks assigned to him
		
		retval = ''
		for day in r:
			if len(day.work_item.all()) != 0:
				retval += '''<b>%s</b><br><a href="%s">%s</a><br>%s<br><hr>''' % ( day.work_item.all()[0].project.all()[0].project_number, day.get_absolute_url(), day.work_item.all()[0].title, day.get_day_type_display() )
			elif len(day.wip_item.all()) != 0:
				retval += '''<b>WIP Item</b><br><a href="%s">%s</a><br>%s<br><hr>''' % ( day.wip_item.all()[0].get_absolute_url(), day.wip_item.all()[0],  day.get_day_type_display() )
			
		return retval	
register.simple_tag(get_project_task_for_day)


def get_edit_rota_form_for_user(person, day):

	try:
		r = RotaItem.objects.get(date=day, person=person)
		form = RotaItemForm(instance=r)
	except RotaItem.DoesNotExist:
		form = RotaItemForm()
	
	str = '''%s_%s''' % ( person, day.strftime("%Y%m%d") )
	form.auto_id = str + "_%s"
	return form['activity']
register.simple_tag(get_edit_rota_form_for_user)
