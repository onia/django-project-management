from django.contrib.auth.models import User


from piston.handler import BaseHandler
from piston.utils import rc, require_mime, require_extended, validate
import settings

from projects.models import *
from projects.forms import EditPID, CompanyForm
from projects.misc import handle_form_errors, check_project_read_acl, check_project_write_acl, return_json_success, handle_generic_error

import settings
log = settings.get_debug_settings('api-views')

class ProjectResourceHandler(BaseHandler):
    """
    URI: /api/projects/%project_number%/
    VERBS: GET, PUT, DELETE

    Handles a single instance of Project
    """

    allowed_methods = ('GET', 'PUT', 'DELETE')
    model = Project

    def read(self, request, project_number):
        """ View a project """

        log.debug("GET request from user %s for project number %s" % ( request.user, project_number ))
        proj = Project.objects.get(project_number=project_number)

        if not check_project_read_acl(proj, request.user):
            log.debug("Refusing GET request for project %s from user %s" % ( project_number, request.user ))
            return rc.FORBIDDEN
        return proj

    def update(self, request, project_number):
        """ Update the project """

        log.debug("PUT request from user %s for project number %s" % ( request.user, project_number ))
        proj = Project.objects.get(project_number=project_number)
        log.debug("Fetched object from database %s" % proj)

        if not check_project_write_acl(proj, request.user):
            log.debug("Refusing PUT request for project %s from user %s" % ( project_number, request.user ))
            return rc.FORBIDDEN

        form = EditPID(request.POST, instance=proj)
        if form.is_valid():
            t = form.save()
            if request.POST.get('team_managers_placeholder'):
                for id in request.POST['team_managers_placeholder'].split(','):
                    t.team_managers.add(id)
            log.debug('Saving %s back to database' % t)
            t.save()
            return t
        else:
            resp = rc.BAD_REQUEST
            resp.write(form.errors)
            log.debug('Validation errors with %s' % t)
            t.save()
            return resp

    def delete(self, request, project_number):
        """ Put the project into archived state, not actually delete it """

        log.debug("DELETE request from user %s for project number %s" % ( request.user, project_number ))
        proj = Project.objects.get(project_number=project_number)
        log.debug("Fetched object from database %s" % proj)

        if not check_project_write_acl(proj, request.user):
            log.debug("Refusing DELETE request for project %s from user %s" % ( project_number, request.user ))
            return rc.FORBIDDEN

        proj.project_status = 5
        proj.save()
        log.debug("Archived project %s" % proj)
        return rc.ALL_OK

class ProjectListHandler(BaseHandler):
    """ 
    URI: /api/projects/
    VERBS: GET, POST

    Returns a list of projects the user is allowed to see
    """

    allowed_methods  = ('GET', 'POST')
    models = Project

    @validate(EditPID)
    def create(self, request):
        """ Create a new Project """

        log.debug("POST request from user %s to create a new project"% request.user)

        # Only users with the create_project permission can do this
        if 'projects.can_create_project' not in request.user.get_all_permissions():
            log.debug('User %s is not allowed to create projects, DENIED' % request.user)
            return rc.FORBIDDEN

        # Go ahead and create the project....
        form = EditPID(request.POST)
        t = form.save()
        return t


    def read(self, request):
        """ Return a list of projects filtered by ACL """

        log.debug("GET request from user %s for project list" % request.user)
        projects = Project.objects.filter(active=True, read_acl__in=request.user.groups.all()).exclude(project_status=5).distinct()
        return projects

class CompanyListHandler(BaseHandler):
    """
    URI: /api/companies/
    VERBS: GET, POST

    Returns a list of companies
    """

    allowed_methods = ('GET', 'POST')
    models = Company

    def read(self, request):
        """ Return a list of company objects """

        log.debug("GET request from user %s for company list" % request.user)
        return Company.objects.filter(active=True)

    @validate(CompanyForm)
    def create(self, request):
        """ Create a new Company """

        form = CompanyForm(request.POST)
        t = form.save()
        log.debug("Accepting request from user %s to create company %s")
        return t

class TeamManagersListHandler(BaseHandler):
    """
    URL: /api/projects/%project_number%/team_managers/
    VERBS: GET

    Return a list of team managers
    """

    allowed_methods = ('GET',)

    def read(self, request, project_number):

        log.debug("GET request from user %s for project %s team managers" % ( request.user, project_number ))
        proj = Project.objects.get(project_number=project_number)

        if not check_project_read_acl(proj, request.user):
            log.debug("Refusing GET request for project %s from user %s" % ( project_number, request.user ))
            return rc.FORBIDDEN
        return User.objects.filter(id__in=proj.team_managers.all()).distinct().order_by('first_name')


class NonTeamManagersListHandler(BaseHandler):
    """
    URL: /api/projects/%project_number%/non_team_managers/
    VERBS: GET

    Return a list of users associated with the project but are not team leaders
    """

    allowed_methods = ('GET',)

    def read(self, request, project_number):

        log.debug("GET request from user %s for project %s non team managers" % ( request.user, project_number ))
        proj = Project.objects.get(project_number=project_number)

        if not check_project_read_acl(proj, request.user):
            log.debug("Refusing GET request for project %s from user %s" % ( project_number, request.user ))
            return rc.FORBIDDEN
        return User.objects.filter(is_active=True, groups__in=proj.read_acl.all()).exclude(id__in=proj.team_managers.all()).distinct().order_by('first_name')


class ResourcesListHandler(BaseHandler):
    """
    URL: /api/projects/%project_number%/resources/
    VERBS: GET

    Return a list of users associated with the project via the read_acl
    """

    allowed_methods = ('GET',)

    def read(self, request, project_number):

        log.debug("GET request from user %s for project %s resources" % ( request.user, project_number ))
        proj = Project.objects.get(project_number=project_number)

        if not check_project_read_acl(proj, request.user):
            log.debug("Refusing GET request for project %s from user %s" % ( project_number, request.user ))
            return rc.FORBIDDEN
        return User.objects.filter(is_active=True, groups__in=proj.read_acl.all()).distinct().order_by('first_name')

