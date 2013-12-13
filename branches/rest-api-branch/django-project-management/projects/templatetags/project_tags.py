import datetime

from django import template
from django.contrib.auth.models import User, Group
from django.template.defaultfilters import linebreaks
try:
	from projects.models import Project, ExecutiveSummary
except:
	pass
from wbs.models import WorkItem

register = template.Library()


def get_css_for_permissions(user, project):
	allow_access = None
	for group in user.groups.all():
		if group in project.write_acl.all():
			allow_access = True

	if allow_access:
		return '''display: inline;'''
	else:
		return '''display: none;'''
register.simple_tag(get_css_for_permissions)
		
def get_predicted_completion_date(project):
	return 'Not implemented yet'
register.simple_tag(get_predicted_completion_date)	


# RAG Status --------------------------------------------------	
def get_project_rag_status(project):
	status, error_list = is_project_up_to_date(project)
	return error_list
register.simple_tag(get_project_rag_status)

def get_project_rag_status_brief(project):
	status, error_list = is_project_up_to_date(project)
	if status == 'rag_status_green': return 'OK'
	elif status == 'rag_status_red': return 'Late'
	elif status == 'rag_status_amber': return 'In Danger'
	elif status == 'rag_status_blue': return 'Unknown'
	return error_list
register.simple_tag(get_project_rag_status_brief)


def get_project_rag_status_css_class(project):
	status, error_list = is_project_up_to_date(project)
	return status
register.simple_tag(get_project_rag_status_css_class)



# -----------------------------------------------------------


# Documentation Status ----------------------------------------
def get_project_documentation_status(project):
	status, error_list = is_project_documentation_complete(project)
	return error_list
register.simple_tag(get_project_documentation_status)


def get_project_documentation_status_brief(project):
	status, error_list = is_project_documentation_complete(project)
	if status == 'documentation_status_green': return 'OK'
	elif status == 'documentation_status_red': return 'Incomplete'
	return error_list
register.simple_tag(get_project_documentation_status_brief)

def get_project_documentation_status_css_class(project):
	status, error_list = is_project_documentation_complete(project)
	return status
register.simple_tag(get_project_documentation_status_css_class)
# -----------------------------------------------------------

def is_project_documentation_complete(project):

	# This RAG evaluation only returns RED or GREEN depending on the status of documentation
	# We evaluate the completion of all Project Initiation items, and we also check for the presence of 
	# at least ONE risk and ONE deliverable. If those are met return Green; if not return Red

	if project.project_status == 0:		# If the project is Proposed or On Hold
		return 'rag_status_grey', 'Proposed'
	elif project.project_status == 1:
		return 'rag_status_grey', 'Draft'
	elif project.project_status == 3:
		return 'rag_status_grey', 'On Hold'
	elif project.project_status == 6:
		return 'rag_status_grey', 'Informational'

	error_list = ''
	status = 'documentation_status_red'

	for attribute in ['project_description', 'business_case', 'business_benefits', 'project_scope', 'exclusions', 
						'assumptions']:
		if eval('''project.%s''' % attribute) == '':
			error_list += '''<li>%s is incomplete</li>''' % project._meta.get_field(attribute).verbose_name

	if len(project.deliverables.all()) < 1:	
		error_list += '<li>Less than 2 Deliverables defined</li>'

	if len(project.risks.all()) < 1:
		error_list += '<li>Less than 2 Risks defined</li>'

			
	if error_list == '':
		error_list = '<li>Complete</li>'
		status = 'documentation_status_green'
	
	return status, error_list

def is_project_up_to_date(project):
	
	# This RAG evaluation returns RED, AMBER, GREEN, GREY or BLUE depending on the allocation of tasks and the completeness
	# of assigned work

	if project.project_status == 0:		# If the project is Proposed or On Hold
		return 'rag_status_grey', 'Proposed'
	elif project.project_status == 1:
		return 'rag_status_grey', 'Draft'
	elif project.project_status == 3:
		return 'rag_status_grey', 'On Hold'
	elif project.project_status == 6:
		return 'rag_status_grey', 'Informational'

	status = 'rag_status_blue' # Lets start off by assuming we can't successfully determine the status

	# Firstly, if less than 25% of tasks have a finish date set we will mark the project as BLUE and return here
	number_of_tasks = WorkItem.objects.filter(active=True, project=project).count()
	tasks_with_finish_dates = WorkItem.objects.filter(active=True, project=project, finish_date__isnull=False)
	number_of_tasks_with_finish_dates = tasks_with_finish_dates.count()
	try:
		percentage_with_finish_dates = float(1.0*number_of_tasks_with_finish_dates/number_of_tasks)*100
	except ZeroDivisionError:
		percentage_with_finish_dates = 0

	if percentage_with_finish_dates < 25:
		error_list = '<li>Not enough tasks have finish dates</li>'''
		return status, error_list  # Exit point here....
	
	# If we have gotten this far we should be able to determine a RED, AMBER, GREEN Status... let's assume we are going to go green
	status = 'rag_status_green'

	now = datetime.datetime.now()										# now = datetime.datetime(2009, 9, 14, 17, 21, 29, 220270)
	today = datetime.date( now.year, now.month, now.day )
	we_had_a_red = False
	number_of_late_tasks = 0
	for task in tasks_with_finish_dates:	

		if task.percent_complete < 100:


			# Is the task more than 5 days late?
			diff = now - task.finish_date
			if diff.days > 5:
				number_of_late_tasks += 1
				status = 'rag_status_red'
				we_had_a_red = True

			elif diff.days > 4 and diff.days > 0:
				number_of_late_tasks += 1
				status = 'rag_status_amber'

	# We may have iterated through all the tasks... found a red task and set status to rag_status_red and then 
	# found another task which is rag_status_amber and forgot about it. If we had a red task at all set the status to red
	if we_had_a_red:
		status = 'rag_status_red'
	
	if number_of_late_tasks == 0: error_list = 'All tasks are up to date'
	elif number_of_late_tasks == 1: error_list = '1 task is late'
	else: error_list = '''%s tasks are late''' % number_of_late_tasks
	return status, error_list

def get_task_rag_status(task):	

	now = datetime.datetime.now()										# now = datetime.datetime(2009, 9, 14, 17, 21, 29, 220270)
	today = datetime.date( now.year, now.month, now.day )
	status = ''

	if task.percent_complete < 100:
		if task.finish_date:

			# Is the task more than 5 days late?
			diff = now - task.finish_date
			if diff.days > 5:
				status = 'rag_status_red'
			elif diff.days > 4 and diff.days > 0:
				status = 'rag_status_amber'

	return status
register.simple_tag(get_task_rag_status)

def get_project_percent_complete(project):

	# A simple percentage calculation.. how many tasks are there
	# and how complete is each task?

	number_of_tasks = len(project.work_items.all())
	progress_complete = 0

	for task in project.work_items.all():
		if not task.percent_complete:
			task.percent_complete = 0
		progress_complete += int(task.percent_complete)


	one_percent = int(number_of_tasks) 
	
	try:	
		ret = progress_complete / one_percent
	except ZeroDivisionError: # occurs when a project has no tasks at all
		ret = 0
	return ret
register.simple_tag(get_project_percent_complete)

def get_initials_for_user(user):
	
	if user.first_name and user.last_name:
		str = '''%s%s''' % ( user.first_name[0], user.last_name[0] )
		return str.upper()
	else:
		return user.username
register.simple_tag(get_initials_for_user)

def get_latest_project_exec_summary(project):
	summary = ExecutiveSummary.objects.filter(project=project)
	if len(summary) == 0:
		return ''
	else:
		return linebreaks(summary[0].summary)
register.simple_tag(get_latest_project_exec_summary)


def get_tagline_subheading():
	import settings
	return getattr(settings, 'TAGLINE_SUBHEADING', 'Django Project Management')
register.simple_tag(get_tagline_subheading)

def get_tagline_footer():
	import settings
	return getattr(settings, 'TAGLINE_FOOTER', '<a href="http://code.google.com/p/django-project-management/">Django Project Management</a>')
register.simple_tag(get_tagline_footer)

def get_tagline_title():
	import settings
	return getattr(settings, 'TAGLINE_TITLE', 'Django Project Management')
register.simple_tag(get_tagline_title)
