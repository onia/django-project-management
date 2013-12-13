import time

from django.contrib.auth.models import User
from piston.handler import BaseHandler
from piston.utils import rc, require_mime, require_extended, validate

from projects.models import *
from issues.forms import IssueForm
from issues.models import *
from projects.misc import handle_form_errors, check_project_read_acl, check_project_write_acl, return_json_success, handle_generic_error

import settings
log = settings.get_debug_settings('issue-api-views')

class IssueResourceHandler(BaseHandler):
    """
    URI: /api/issues/%project_number%/%issue_id%/
    VERBS: GET, PUT, DELETE

    Handles a single instance of Issue
    """

    allowed_methods = ('GET', 'PUT', 'DELETE')
    model = Issue

    def read(self, request, project_number, issue_id):
        """ View an issue """

        log.debug("GET request from user %s for issue id %s" % ( request.user, issue_id ))
        proj = Project.objects.get(project_number=project_number)
        issue = Issue.objects.get(id=issue_id)

        if not check_project_read_acl(proj, request.user):
            log.debug("Refusing GET request for project %s from user %s" % ( project_number, request.user ))
            return rc.FORBIDDEN
        return issue

    def update(self, request, project_number, issue_id):
        """ Update the issue """

        log.debug("PUT request from user %s for issue id %s" % ( request.user, issue_id))
        proj = Project.objects.get(project_number=project_number)
        issue = Issue.objects.get(id=issue_id)
        log.debug("Fetched object from database %s" % issue)

        if not check_project_write_acl(proj, request.user):
            log.debug("Refusing PUT request for project %s from user %s" % ( project_number, request.user ))
            return rc.FORBIDDEN

        form = IssueForm(request.POST, instance=issue)
        if form.is_valid():
            t = form.save(commit=False)
            if request.POST['update'] != '':                        
                if not request.user.get_full_name():
                    update_name = request.user.username
                else:
                    update_name = request.user.get_full_name()
                    t.history = '''\n\n------Updated by %s on %s------\n\n%s\n\n%s''' % ( update_name, time.strftime("%Y-%m-%d %H:%M"),
                    form.cleaned_data.get('update'), issue.history )
            log.debug('Saving %s back to database' % t)
            t.save()
            return t
        else:
            resp = rc.BAD_REQUEST
            resp.write(form.errors)
            log.debug('Validation errors with %s' % t)
            t.save()
            return resp

    def delete(self, request, project_number, risk_number):
        """ Disassociate the issue from the project, not actually delete it """

        log.debug("DELETE request from user %s for issue id %s" % ( request.user, issue_id))
        proj = Project.objects.get(project_number=project_number)
        issue = Issue.objects.get(id=issue_id)
        log.debug("Fetched object from database %s" % issue)

        if not check_project_write_acl(proj, request.user):
            log.debug("Refusing DELETE request for risk %s from user %s" % ( risk_number, request.user ))
            return rc.FORBIDDEN

        proj.issues.remove(issue)
        proj.save()
        log.debug("Deleted issue %s" % issue)
        return rc.ALL_OK

class IssueListHandler(BaseHandler):
    """ 
    URI: /api/issues/%project_number%/
    VERBS: GET, POST

    Returns a list of issues associated with a project
    """

    allowed_methods  = ('GET', 'POST')
    models = Issue

    @validate(IssueForm)
    def create(self, request, project_number):
        """ Create a new Issue """

        log.debug("POST request from user %s to create a new issue" % request.user)
        proj = Project.objects.get(project_number=project_number)

        if not check_project_write_acl(proj, request.user):
            log.debug("Refusing POST request for project %s from user %s" % ( project_number, request.user ))
            return rc.FORBIDDEN

        # Go ahead and create the issue....
        form = IssueForm(request.POST)
        t = form.save(commit=False)
        t.save()
        proj.issues.add(t)
        proj.save()
        return t


    def read(self, request, project_number):
        """ Return a list of issues associated with projects filtered by ACL """

        log.debug("GET request from user %s for risk list" % request.user)
        proj = Project.objects.get(project_number=project_number)

        if not check_project_read_acl(proj, request.user):
            log.debug("Refusing GET request for project list %s from user %s" % ( project_number, request.user ))
            return rc.FORBIDDEN

        return proj.issues.all()

class UserIssueListHandler(BaseHandler):
    """ 
    URI: /api/issues/
    VERBS: GET

    Returns a list of issues associated with the request.user account
    """

    allowed_methods  = ('GET',)
    models = Issue

    def read(self, request):
        """ Return a list of Issue objects that are related to the user account.
        Filter Issues that aren't associated with any projects """

        issue_list = []
        projects = Project.objects.filter(active=True, read_acl__in=request.user.groups.all()).exclude(project_status=5).distinct()
        for p in projects:
            issue_list += p.issues.all()
        return issue_list

