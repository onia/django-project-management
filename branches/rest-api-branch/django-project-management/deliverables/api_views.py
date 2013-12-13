from django.contrib.auth.models import User
from piston.handler import BaseHandler
from piston.utils import rc, require_mime, require_extended, validate

from projects.models import *
from deliverables.forms import DeliverableForm
from deliverables.models import *
from projects.misc import handle_form_errors, check_project_read_acl, check_project_write_acl, return_json_success, handle_generic_error

import settings
log = settings.get_debug_settings('deliverable-api-views')

class DeliverableResourceHandler(BaseHandler):
    """
    URI: /api/deliverables/%project_number%/%deliverable_id%/
    VERBS: GET, PUT, DELETE

    Handles a single instance of Deliverable
    """

    allowed_methods = ('GET', 'PUT', 'DELETE')
    model = Deliverable
    exclude = []

    def read(self, request, project_number, deliverable_id):
        """ View a deliverable """

        log.debug("GET request from user %s for deliverable %s" % ( request.user, deliverable_id ))
        proj = Project.objects.get(project_number=project_number)
        deliverable = Deliverable.objects.get(id=deliverable_id)

        if not check_project_read_acl(proj, request.user):
            log.debug("Refusing GET request for project %s from user %s" % ( project_number, request.user ))
            return rc.FORBIDDEN
        return deliverable

    def update(self, request, project_number, deliverable_id):
        """ Update the deliverable """

        log.debug("PUT request from user %s for deliverable %s" % ( request.user, deliverable_id ))
        proj = Project.objects.get(project_number=project_number)
        deliverable = Deliverable.objects.get(id=deliverable_id)
        log.debug("Fetched object from database %s" % deliverable)

        if not check_project_write_acl(proj, request.user):
            log.debug("Refusing PUT request for project %s from user %s" % ( project_number, request.user ))
            return rc.FORBIDDEN

        form = DeliverableForm(request.POST, instance=deliverable)
        if form.is_valid():
            t = form.save()
            log.debug('Saving %s back to database' % t)
            return t
        else:
            resp = rc.BAD_REQUEST
            resp.write(form.errors)
            log.debug('Validation errors with %s' % t)
            return resp

    def delete(self, request, project_number, deliverable_id):
        """ Disassociate the deliverable from the project, not actually delete it """

        log.debug("DELETE request from user %s for deliverable %s" % ( request.user, deliverable_id ))
        proj = Project.objects.get(project_number=project_number)
        deliverable = Deliverable.objects.get(id=deliverable_id)
        log.debug("Fetched object from database %s" % deliverable)

        if not check_project_write_acl(proj, request.user):
            log.debug("Refusing DELETE request for deliverable %s from user %s" % ( deliverable_id, request.user ))
            return rc.FORBIDDEN

        proj.deliverables.remove(deliverable)
        proj.save()
        log.debug("Deleted deliverable %s" % deliverable)
        return rc.ALL_OK

class DeliverableListHandler(BaseHandler):
    """ 
    URI: /api/deliverables/%project_number%/
    VERBS: GET, POST

    Returns a list of deliverable associated with a project
    """

    allowed_methods  = ('GET', 'POST')
    models = Deliverable
    exclude = []

    @validate(DeliverableForm)
    def create(self, request, project_number):
        """ Create a new Deliverable """

        log.debug("POST request from user %s to create a new deliverable" % request.user)
        proj = Project.objects.get(project_number=project_number)

        if not check_project_write_acl(proj, request.user):
            log.debug("Refusing POST request for project %s from user %s" % ( project_number, request.user ))
            return rc.FORBIDDEN

        # Go ahead and create the deliverable....
        form = DeliverableForm(request.POST)
        t = form.save()
        proj.deliverables.add(t)
        proj.save()
        return t


    def read(self, request, project_number):
        """ Return a list of deliverables associated with projects filtered by ACL """

        log.debug("GET request from user %s for deliverable list" % request.user)
        proj = Project.objects.get(project_number=project_number)

        if not check_project_read_acl(proj, request.user):
            log.debug("Refusing GET request for project list %s from user %s" % ( project_number, request.user ))
            return rc.FORBIDDEN

        return proj.deliverables.all()

