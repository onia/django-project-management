import time

from django.contrib.auth.models import User
from piston.handler import BaseHandler
from piston.utils import rc, require_mime, require_extended, validate

from projects.models import *
from risks.forms import RiskForm
from risks.models import *
from projects.misc import handle_form_errors, check_project_read_acl, check_project_write_acl, return_json_success, handle_generic_error

import settings
log = settings.get_debug_settings('risk-api-views')

class RiskResourceHandler(BaseHandler):
    """
    URI: /api/risks/%project_number%/%risk_number%/
    VERBS: GET, PUT, DELETE

    Handles a single instance of Risk
    """

    allowed_methods = ('GET', 'PUT', 'DELETE')
    model = Risk

    def read(self, request, project_number, risk_number):
        """ View a risk """

        log.debug("GET request from user %s for risk number %s" % ( request.user, risk_number ))
        proj = Project.objects.get(project_number=project_number)
        risk = Risk.objects.get(risk_number=risk_number)

        if not check_project_read_acl(proj, request.user):
            log.debug("Refusing GET request for project %s from user %s" % ( project_number, request.user ))
            return rc.FORBIDDEN
        return risk

    def update(self, request, project_number, risk_number):
        """ Update the risk """

        log.debug("PUT request from user %s for risk number %s" % ( request.user, risk_number ))
        proj = Project.objects.get(project_number=project_number)
        risk = Risk.objects.get(risk_number=risk_number)
        log.debug("Fetched object from database %s" % risk)

        if not check_project_write_acl(proj, request.user):
            log.debug("Refusing PUT request for project %s from user %s" % ( project_number, request.user ))
            return rc.FORBIDDEN

        form = RiskForm(request.POST, instance=risk)
        if form.is_valid():
            t = form.save(commit=False)
            t.rating = _calculate_risk(t.probability, t.impact)
            if request.POST['update'] != '':                        
                if not request.user.get_full_name():
                    update_name = request.user.username
                else:
                    update_name = request.user.get_full_name()
                    t.history = '''\n\n------Updated by %s on %s------\n\n%s\n\n%s''' % ( update_name, time.strftime("%Y-%m-%d %H:%M"),
                    form.cleaned_data.get('update'), risk.history )
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
        """ Disassociate the risk from the project, not actually delete it """

        log.debug("DELETE request from user %s for risk number %s" % ( request.user, risk_number ))
        proj = Project.objects.get(project_number=project_number)
        risk = Risk.objects.get(risk_number=risk_number)
        log.debug("Fetched object from database %s" % risk)

        if not check_project_write_acl(proj, request.user):
            log.debug("Refusing DELETE request for risk %s from user %s" % ( risk_number, request.user ))
            return rc.FORBIDDEN

        proj.risks.remove(risk)
        proj.save()
        log.debug("Deleted risk %s" % risk)
        return rc.ALL_OK

class RiskListHandler(BaseHandler):
    """ 
    URI: /api/risks/%project_number%/
    VERBS: GET, POST

    Returns a list of risks associated with a project
    """

    allowed_methods  = ('GET', 'POST')
    models = Risk

    @validate(RiskForm)
    def create(self, request, project_number):
        """ Create a new Risk """

        log.debug("POST request from user %s to create a new risk" % request.user)
        proj = Project.objects.get(project_number=project_number)

        if not check_project_write_acl(proj, request.user):
            log.debug("Refusing POST request for project %s from user %s" % ( project_number, request.user ))
            return rc.FORBIDDEN

        # Go ahead and create the risk....
        form = RiskForm(request.POST)
        t = form.save(commit=False)
        t.risk_number = '''RISK-%s-%s''' % (request.user.username[:2].upper(), time.strftime("%Y%m%d%H%M"))
        t.rating = _calculate_risk(t.probability, t.impact)
        t.save()
        proj.risks.add(t)
        proj.save()
        return t


    def read(self, request, project_number):
        """ Return a list of risks associated with projects filtered by ACL """

        log.debug("GET request from user %s for risk list" % request.user)
        proj = Project.objects.get(project_number=project_number)

        if not check_project_read_acl(proj, request.user):
            log.debug("Refusing GET request for project list %s from user %s" % ( project_number, request.user ))
            return rc.FORBIDDEN

        return proj.risks.all()

class UserRiskListHandler(BaseHandler):
    """ 
    URI: /api/risks/
    VERBS: GET

    Returns a list of risks associated with the request.user account
    """

    allowed_methods  = ('GET',)
    models = Risk

    def read(self, request):
        """ Return a list of Risk objects that are related to the user account.
        Filter Risks that aren't associated with any projects """

        risk_list = []
        projects = Project.objects.filter(active=True, read_acl__in=request.user.groups.all()).exclude(project_status=5).distinct()
        risks = Risk.objects.filter(project__in=projects).filter(owner=request.user)
        return risks


def _calculate_risk(probability, impact):
    """ Returns a risk priority based on probability, impact """

    return (probability * impact ) / 2                      
        

