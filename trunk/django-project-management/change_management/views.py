# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, Template, RequestContext
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.db.models import Q
from projects.models import *
from projects.views import updateLog
from change_management.models import *
from change_management.forms import *
import time

@login_required
def viewRFPC(request, projectNumber):

	project = Project.objects.get(projectNumber=projectNumber)
	rfpcs = RequestForChange.objects.filter(project_changes=project)
	# Generate a unique RFPC number
	rfpcNumber = '''RFPC-%s-%s''' % ( projectNumber, time.strftime("%Y%m%d%H%M"))
	form = RFPCForm(initial={'requestor': request.user.id})

	return render_to_response('change_management/view-rfpcs.html', {'project': project, 'rfpcs': rfpcs, 'form': form }, context_instance=RequestContext(request))

@login_required
def addRFPC(request, projectNumber):

	project = Project.objects.get(projectNumber=projectNumber)
	if request.method == 'POST':
		form = RFPCForm(request.POST)
		if form.is_valid():
			t = form.save()
			t.save()
			project.rfpc.add(t)
			project.save()
			request.user.message_set.create(message='''RFPC %s Registered''' % t.slug)
			updateLog(request, projectNumber, 'RFPC %s Registered' % t.slug)
			return HttpResponseRedirect('/Projects/%s/RFPC' % project.projectNumber)
		else:
			pass
	else:
		form = RFPCForm()
	return render_to_response('change_management/view-rfpcs.html', { 'form': form, 'project': project }, context_instance=RequestContext(request))

@login_required
def editRFPC(request, projectNumber, rfpcSlug):

	project = Project.objects.get(projectNumber=projectNumber)
	rfpc = RequestForChange.objects.get(slug=rfpcSlug)
	if request.method == 'POST':
		form = RFPCForm(request.POST, instance=rfpc)
		if form.is_valid():
			t = form.save()
			t.save()
			request.user.message_set.create(message='''RFPC %s Edited''' % t.slug)
			for change in form.changed_data:
				if change != 'slug': updateLog(request, projectNumber, '%s changed to %s' % ( change, eval('''t.%s''' % change)))
			return HttpResponseRedirect('/Projects/%s/RFPC' % project.projectNumber)
		else:
			pass
	else:
		form = RFPCForm(instance=rfpc)
	return render_to_response('change_management/edit-rfpc.html', { 'form': form, 'project': project, 'rfpc': rfpc }, context_instance=RequestContext(request))

@login_required
def deleteRFPC(request, projectNumber, rfpcSlug):

	project = Project.objects.get(projectNumber=projectNumber)
	project.rfpc.remove(rfpc)
	request.user.message_set.create(message='''RFPC %s Deleted''' % rfpc.slug)
	return HttpResponseRedirect('/Projects/%s/RFPC' % project.projectNumber)
	
			
		

	
