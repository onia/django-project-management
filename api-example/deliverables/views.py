# Create your views here.
import simplejson as json

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, Template, RequestContext
from django.template.loader import get_template
from django.template.defaultfilters import slugify
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q
from projects.models import *
from projects.views import updateLog
from deliverables.forms import *
from projects.misc import handle_form_errors, check_project_read_acl, check_project_write_acl, return_json_success, handle_generic_error, user_has_write_access

@login_required
def add_deliverable(request, project_number):

        # Some security - only allow users to view objects they are allowed to via read_acl
        project = get_object_or_404(Project, project_number=project_number)
        check_project_read_acl(project, request.user)   # Will return Http404 if user isn't allowed to view project
        if request.method == 'POST':
                form = DeliverableForm(request.POST)
                if form.is_valid():
                        t = form.save()
                        t.save()
                        project.deliverables.add(t)
                        project.save()
                        request.user.message_set.create(message='''Deliverable %s Registered''' % t.id)
                        updateLog(request, project_number, '''Deliverable %s Registered''' % t.id)
                        return HttpResponse( return_json_success() )
                else:
                        return HttpResponse( handle_form_errors(form.errors))

@login_required
def edit_deliverable(request, project_number, deliverable_id):

        project = Project.objects.get(project_number=project_number)
        deliverable = Deliverable.objects.get(id=deliverable_id)
        if request.method == 'POST':
                form = DeliverableForm(request.POST, instance=deliverable)
                if form.is_valid():
                        t = form.save()
                        t.save()
                        request.user.message_set.create(message='''Deliverable %s Edited''' % t.id)
                        for change in form.changed_data:
                                updateLog(request, project_number, '''%s changed to %s''' % ( change, eval('''t.%s''' % change)))               
                        return HttpResponse( return_json_success() )
                else:
                        return HttpResponse( handle_form_errors(form.errors))

@login_required
def delete_deliverable(request, project_number, deliverable_id):

        # Some security - only allow users to view objects they are allowed to via read_acl
        project = get_object_or_404(Project, project_number=project_number)
        check_project_read_acl(project, request.user)   # Will return Http404 if user isn't allowed to view project
        
        if user_has_write_access(project, request.user):
                deliverable = Deliverable.objects.get(id=deliverable_id)
                project.deliverables.remove(deliverable)
                project.save()
                return HttpResponse( return_json_success() )
        else:
                return HttpResponse( handle_generic_error("Sorry - you don't have sufficient access to update the project"))
        
@login_required
def view_deliverables(request, project_number):
        project = Project.objects.get(project_number=project_number)
        return HttpResponse( serializers.serialize('json', project.deliverables.all()))
        
@login_required
def view_deliverable(request, project_number, deliverable_id):
        deliverable = Deliverable.objects.get(id=deliverable_id)
        JSONSerializer = serializers.get_serializer('json')
        j = JSONSerializer()
        j.serialize([deliverable], fields=('description', 'acceptance_criteria', 'deliverable_tester', 'testing_method', 'expected_result', 'rpo', 'rto'))
        
        return HttpResponse( '''{ success: true, data: %s }''' % json.dumps(j.objects[0]['fields']))



