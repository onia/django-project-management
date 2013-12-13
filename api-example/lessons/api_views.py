from django.contrib.auth.models import User
from piston.handler import BaseHandler
from piston.utils import rc, require_mime, require_extended, validate

from projects.models import *
from lessons.forms import LessonForm
from lessons.models import *
from projects.misc import handle_form_errors, check_project_read_acl, check_project_write_acl, return_json_success, handle_generic_error

import settings
log = settings.get_debug_settings('lessons-api-views')

class LessonResourceHandler(BaseHandler):
    """
    URI: /api/lessons/%project_number%/%lesson_id%/
    VERBS: GET, PUT, DELETE

    Handles a single instance of Lesson
    """

    allowed_methods = ('GET', 'PUT', 'DELETE')
    model = LessonLearnt

    def read(self, request, project_number, lesson_id):
        """ View a lesson """

        log.debug("GET request from user %s for lesson %s" % ( request.user, lesson_id ))
        proj = Project.objects.get(project_number=project_number)
        lesson = LessonLearnt.objects.get(id=lesson_id)

        if not check_project_read_acl(proj, request.user):
            log.debug("Refusing GET request for project %s from user %s" % ( project_number, request.user ))
            return rc.FORBIDDEN
        return lesson

    def update(self, request, project_number, lesson_id):
        """ Update the lesson """

        log.debug("PUT request from user %s for lesson %s" % ( request.user, lesson_id ))
        proj = Project.objects.get(project_number=project_number)
        lesson = LessonLearnt.objects.get(id=lesson_id)
        log.debug("Fetched object from database %s" % lesson)

        if not check_project_write_acl(proj, request.user):
            log.debug("Refusing PUT request for project %s from user %s" % ( project_number, request.user ))
            return rc.FORBIDDEN

        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            t = form.save()
            log.debug('Saving %s back to database' % t)
            return t
        else:
            resp = rc.BAD_REQUEST
            resp.write(form.errors)
            log.debug('Validation errors with %s' % t)
            return resp

    def delete(self, request, project_number, lesson_id):
        """ Disassociate the lesson from the project, not actually delete it """

        log.debug("DELETE request from user %s for lesson %s" % ( request.user, lesson_id ))
        proj = Project.objects.get(project_number=project_number)
        lesson = LessonLearnt.objects.get(id=lesson_id)
        log.debug("Fetched object from database %s" % lesson)

        if not check_project_write_acl(proj, request.user):
            log.debug("Refusing DELETE request for lesson %s from user %s" % ( lesson_id, request.user ))
            return rc.FORBIDDEN

        proj.lessons.remove(lesson)
        proj.save()
        log.debug("Deleted lesson %s" % lesson)
        return rc.ALL_OK

class LessonListHandler(BaseHandler):
    """ 
    URI: /api/lessons/%project_number%/
    VERBS: GET, POST

    Returns a list of lessons associated with a project
    """

    allowed_methods  = ('GET', 'POST')
    models = LessonLearnt

    @validate(LessonForm)
    def create(self, request, project_number):
        """ Create a new Lesson """

        log.debug("POST request from user %s to create a new lesson" % request.user)
        proj = Project.objects.get(project_number=project_number)

        if not check_project_write_acl(proj, request.user):
            log.debug("Refusing POST request for project %s from user %s" % ( project_number, request.user ))
            return rc.FORBIDDEN

        # Go ahead and create the lesson....
        form = LessonForm(request.POST)
        t = form.save()
        proj.lessons.add(t)
        proj.save()
        return t


    def read(self, request, project_number):
        """ Return a list of Lessons associated with projects filtered by ACL """

        log.debug("GET request from user %s for lesson list" % request.user)
        proj = Project.objects.get(project_number=project_number)

        if not check_project_read_acl(proj, request.user):
            log.debug("Refusing GET request for project list %s from user %s" % ( project_number, request.user ))
            return rc.FORBIDDEN

        return proj.lessons.all()

