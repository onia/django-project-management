# Create your views here
import simplejson as json

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, Template, RequestContext
from django.template.loader import get_template
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q
from projects.models import *
from projects.views import updateLog
from risks.forms import *
from projects.misc import handle_form_errors, check_project_read_acl, check_project_write_acl, return_json_success, handle_generic_error
import time

@login_required
def add_risk(request, project_number):

        # Some security - only allow users to view objects they are allowed to via read_acl
        project = get_object_or_404(Project, project_number=project_number)
        check_project_read_acl(project, request.user)   # Will return Http404 if user isn't allowed to view project

        if request.method == 'POST':
                form = RiskForm(request.POST)
                if form.is_valid():
                        t = form.save(commit=False)
                        t.risk_number = '''RISK-%s-%s''' % (request.user.username[:2].upper(), time.strftime("%Y%m%d%H%M"))
                        t.rating = _calculate_risk(t.probability, t.impact)
                        t.save()
                        project.risks.add(t)
                        project.save()
                        request.user.message_set.create(message='''Risk %s Registered''' % t.risk_number)
                        updateLog(request, project.project_number, '''Risk %s Registered''' % t.risk_number)
                        return HttpResponse( return_json_success() )
                else:
                        return HttpResponse( handle_form_errors(form.errors))

@login_required
def get_risk_number(request):
        ret = [ {} ]
        ret[0]['risk_number'] = '''RISK-%s-%s''' % (request.user.username[:2].upper(), time.strftime("%Y%m%d%H%M"))
        return HttpResponse(json.dumps(ret))
        
@login_required
def edit_risk(request, project_number, risk_id):

    risk = Risk.objects.get(id=risk_id)
    project = Project.objects.get(project_number=project_number)
        
    if request.method == 'POST':
        form = RiskForm(request.POST, instance=risk)
        if form.is_valid():
            t = form.save(commit=False)
            t.rating = _calculate_risk(t.probability, t.impact)
            if request.POST['update'] != '':                        
                if request.user.get_full_name() == '':
                    update_name = request.user.username
                else:
                    update_name = request.user.get_full_name()
                    t.history = '''\n\n------Updated by %s on %s------\n\n%s\n\n%s''' % ( update_name, time.strftime("%Y-%m-%d %H:%M"),
                    form.cleaned_data.get('update'), risk.history )
            t.save()
            request.user.message_set.create(message='''Risk %s Edited''' % t.risk_number)
            return HttpResponse( return_json_success() )
        else:
            return HttpResponse( handle_form_errors(form.errors))

@login_required
def delete_risk(request, project_number, risk_id):

        project = Project.objects.get(project_number=project_number)
        try:
                risk = Risk.objects.get(id=risk_id)
        except Risk.DoesNotExist:
                return HttpResponse( handle_generic_error("Risk does not exist"))
        project.risks.remove(risk)
        project.save()
        return HttpResponse( return_json_success() )
        
def _calculate_risk(probability, impact):
        return (probability * impact ) / 2                      
        
@login_required
def view_risks(request, project_number):
        project = Project.objects.get(project_number=project_number)
        return HttpResponse( serializers.serialize('json', project.risks.all(),
            relations={'owner': {'fields': ('username',), 'extras':
                ('get_full_name',)}}, extras=('get_history_html',), display=['status', 'counter_measure']))

@login_required
def view_risk(request, project_number, risk_id):
        risk = Risk.objects.get(id=risk_id)
        JSONSerializer = serializers.get_serializer('json')
        j = JSONSerializer()
        j.serialize([risk], fields=('risk_number', 'description', 'owner', 'probability', 'impact', 'rating', 'counter_measure', 'status', 'history'))
        
        return HttpResponse( '''{ success: true, data: %s }''' % json.dumps(j.objects[0]['fields']))
        
