# Create your views here.
import os
import simplejson as json
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, Template, RequestContext
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.db.models import Q
from projects.models import *
from deliverables.models import *
from risks.models import *
from files.forms import *
from backends.pdfexport import render_to_pdf
import settings
from projects.misc import handle_form_errors, check_project_read_acl, check_project_write_acl, return_json_success, handle_generic_error, user_has_write_access


@login_required
def project_pid(request, project_number):

        project = Project.objects.get(project_number=project_number)
        return render_to_pdf('files/pid.html', { 'project': project, 'files': settings.STATIC_DOC_ROOT, 'title': project.project_number }, filename="%s_PROJECT_INITIATION_DOCUMENT.pdf" % project.project_number )

@login_required
def risk_register(request, project_number):

        project = Project.objects.get(project_number=project_number)
        return render_to_pdf('files/risk_register.html', { 'project': project, 'files': settings.STATIC_DOC_ROOT, 'title': project.project_number, 'paper_orientation': 'landscape' }, filename="%s_RISK_REGISTER.pdf" % project.project_number )


@login_required
def gantt_chart(request, project_number):

        project = Project.objects.get(project_number=project_number)
        #return render_to_pdf('files/gantt.html', { 'project': project, 'files': settings.STATIC_DOC_ROOT, 'title': project.project_number, 'paper_size': 'a3', 'paper_orientation': 'landscape' }, filename="%s_GANTT_CHART.pdf" % project.project_number )
        return render_to_response('files/gantt.html', { 'project': project, 'files': settings.STATIC_DOC_ROOT, 'title': project.project_number, 'paper_size': 'a3', 'paper_orientation': 'landscape' }, context_instance=RequestContext(request))

@login_required
def work_breakdown_structure(request, project_number):

        project = Project.objects.get(project_number=project_number)
        return render_to_pdf('files/wbs.html', { 'project': project, 'files': settings.STATIC_DOC_ROOT, 'title': project.project_number, 'paper_orientation': 'landscape', 'paper_size': 'a3' }, filename="%s_WORK_BREAKDOWN_STRUCTURE.pdf" % project.project_number )
#       return render_to_response('files/wbs.html', { 'project': project, 'files': settings.STATIC_DOC_ROOT, 'title': project.project_number, 'paper_orientation': 'portrait' }, context_instance=RequestContext(request) )


@login_required
def issue_log(request, project_number):

        project = Project.objects.get(project_number=project_number)
        return render_to_pdf('files/issue.html', { 'project': project, 'files': settings.STATIC_DOC_ROOT, 'title': project.project_number, 'paper_orientation': 'landscape', 'paper_size': 'a4' }, filename="%s_ISSUE_LOG.pdf" % project.project_number )
#       return render_to_response('files/wbs.html', { 'project': project, 'files': settings.STATIC_DOC_ROOT, 'title': project.project_number, 'paper_orientation': 'portrait' }, context_instance=RequestContext(request) )

@login_required
def add_file(request, project_number):
        
        project = Project.objects.get(project_number=project_number)
        if request.method == 'POST':
                form = FileForm(request.POST, request.FILES)
                if form.is_valid():
                        t = form.save()
                        project.files.add(t)
                        project.save()
                        return HttpResponse( return_json_success() )
                else:
                        return HttpResponse( handle_form_errors(form.errors))

@login_required
def view_files(request, project_number):
        project = Project.objects.get(project_number=project_number)
        files = []
        files.append({'pk': 0, 'author': '-', 'file_type': '-', 'description': 'Project Initiation Document', 'url': '/Files/%s/PID/' % project.project_number })
        files.append({'pk': 0, 'author': '-', 'file_type': '-', 'description': 'Risk Register', 'url': '/Files/%s/RiskRegister/' % project.project_number })
        files.append({'pk': 0, 'author': '-', 'file_type': '-', 'description': 'Work Breakdown Structure', 'url': '/Files/%s/WBS/' % project.project_number })
        files.append({'pk': 0, 'author': '-', 'file_type': '-', 'description': 'MS Project File (XML Format)', 'url': '/WBS/%s/MSProject/' % project.project_number })
        files.append({'pk': 0, 'author': '-', 'file_type': '-', 'description': 'Issue Log', 'url': '/Files/%s/IssueLog/' % project.project_number })
        for f in project.files.all():
                files.append({'pk': f.id, 'author': f.author.get_full_name(), 'file_type': f.get_file_type_display(), 'url': f.filename.url, 'description': f.description, 'created_date': f.created_date.strftime("%Y-%m-%d %H:%M:%S") })
        return HttpResponse( json.dumps(files))
        
@login_required
def delete_file(request, project_number):
        project = Project.objects.get(project_number=project_number)
        file = ProjectFile.objects.get(id=request.POST['pk'])
        
        if user_has_write_access(project, request.user):
                project.files.remove(file)
                project.save()
                return HttpResponse( return_json_success() )
        else:
                return HttpResponse( handle_generic_error("Sorry - you don't have permission to delete this file"))
                r
        
