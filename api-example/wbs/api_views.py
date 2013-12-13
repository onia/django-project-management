from django.contrib.auth.models import User
from piston.handler import BaseHandler
from piston.utils import rc, require_mime, require_extended, validate

from projects.models import *
from wbs.forms import WBSForm, WBSProjectStage, EngineeringDayForm
from wbs.models import *
from projects.misc import handle_form_errors, check_project_read_acl, check_project_write_acl, return_json_success, handle_generic_error

import settings
log = settings.get_debug_settings('wbs-api-views')

class WBSResourceHandler(BaseHandler):
    """
    URI: /api/wbs/%project_number%/%wbs_id%/
    VERBS: GET, PUT, DELETE

    Handles a single instance of WorkItem
    """

    allowed_methods = ('GET', 'PUT', 'DELETE')
    model = WorkItem

    def read(self, request, project_number, wbs_id):
        """ View a work item """

        log.debug("GET request from user %s for work item %s" % ( request.user, wbs_id ))
        proj = Project.objects.get(project_number=project_number)
        wbs = WorkItem.objects.get(id=wbs_id)

        if not check_project_read_acl(proj, request.user):
            log.debug("Refusing GET request for project %s from user %s" % ( project_number, request.user ))
            return rc.FORBIDDEN
        return wbs

    def update(self, request, project_number, wbs_id):
        """ Update the work item """

        log.debug("PUT request from user %s for work item %s" % ( request.user, wbs_id))
        proj = Project.objects.get(project_number=project_number)
        wbs = WorkItem.objects.get(id=wbs_id)
        log.debug("Fetched object from database %s" % wbs)

        if not check_project_write_acl(proj, request.user):
            log.debug("Refusing PUT request for project %s from user %s" % ( project_number, request.user ))
            return rc.FORBIDDEN

        form = WBSForm(request.POST, instance=wbs)
        if form.is_valid():
            t = form.save(commit=False)
            if request.POST['update'] != '':                        
                if not request.user.get_full_name():
                    update_name = request.user.username
                else:
                    update_name = request.user.get_full_name()
            t.history = '''\n\n------Updated by %s on %s------\n\n%s\n\n%s''' % ( update_name, time.strftime("%Y-%m-%d %H:%M"), form.cleaned_data.get('update'), wbs.history )
            log.debug('Saving %s back to database' % t)
            return t
        else:
            resp = rc.BAD_REQUEST
            resp.write(form.errors)
            log.debug('Validation errors with %s' % t)
            return resp

    def delete(self, request, project_number, wbs_id):
        """ Disassociate the work item from the project, not actually delete it """

        log.debug("DELETE request from user %s for work item %s" % ( request.user, wbs_id ))
        proj = Project.objects.get(project_number=project_number)
        wbs = WorkItem.objects.get(id=wbs_id)
        log.debug("Fetched object from database %s" % wbs)

        if not check_project_write_acl(proj, request.user):
            log.debug("Refusing DELETE request for deliverable %s from user %s" % ( deliverable_id, request.user ))
            return rc.FORBIDDEN

        proj.work_items.remove(wbs)
        proj.save()
        log.debug("Deleted work item %s" % wbs)
        return rc.ALL_OK

class WBSListHandler(BaseHandler):
    """ 
    URI: /api/wbs/%project_number%/
    VERBS: GET, POST

    Returns a list of work items associated with a project
    """

    allowed_methods  = ('GET', 'POST')
    model = WorkItem

    @validate(WBSForm)
    def create(self, request, project_number):
        """ Create a new Work Item """

        log.debug("POST request from user %s to create a new work item" % request.user)
        proj = Project.objects.get(project_number=project_number)

        if not check_project_write_acl(proj, request.user):
            log.debug("Refusing POST request for project %s from user %s" % ( project_number, request.user ))
            return rc.FORBIDDEN

        # Go ahead and create the work item....
        form = WBSForm(request.POST)
        t = form.save()
        proj.work_items.add(t)
        proj.save()
        return t

    def read(self, request, project_number):
        """ Get a list of all Work Items for the project """

        log.debug("GET request from user %s for wbs list" % request.user)
        proj = Project.objects.get(project_number=project_number)

        if not check_project_read_acl(proj, request.user):
            log.debug("Refusing GET request for project list %s from user %s" % ( project_number, request.user ))
            return rc.FORBIDDEN

        return WorkItem.objects.filter(project_stage__project=proj)

class UserWBSListHandler(BaseHandler):
    """ 
    URI: /api/wbs/
    VERBS: GET

    Returns a list of work items associated with an user
    """

    allowed_methods  = ('GET',)
    model = WorkItem

    def read(self, request, project_number):
        """ Return a list of work items associated with projects filtered by ACL """

        log.debug("GET request from user %s for user work item list" % request.user)
        projects = Project.objects.filter(active=True, read_acl__in=request.user.groups.all()).exclude(project_status=5).distinct()
        
        wbs_list = WorkItem.objects.filter(project_stage__project__in=projects)
        return wbs_list 

class StageplanListHandler(BaseHandler):
    """ 
    URL: /api/stageplan/%project_number%/
    VERBS: GET, POST

    Returns a list of Stage Plans associated with a project
    """

    allowed_methods = ('GET', 'POST')
    model = ProjectStage

    @validate(WBSProjectStage)
    def create(self, request, project_number):
        """ Create a new Project Stage """

        log.debug("POST request from user %s to create a new project stage" % request.user)
        proj = Project.objects.get(project_number=project_number)

        if not check_project_write_acl(proj, request.user):
            log.debug("Refusing POST request for project %s from user %s" % ( project_number, request.user ))
            return rc.FORBIDDEN

        # Go ahead and create the project stage....
        form = WBSProjectStage(request.POST)
        t = form.save()
        proj.stage_plan.add(t)
        proj.save()
        return t

    def read(self, request, project_number):
        """ Return a list of project stages associated with projects filtered by ACL """

        log.debug("GET request from user %s for stage plan list" % request.user)
        proj = Project.objects.get(project_number=project_number)

        if not check_project_read_acl(proj, request.user):
            log.debug("Refusing GET request for project list %s from user %s" % ( project_number, request.user ))
            return rc.FORBIDDEN

        return proj.stage_plan.all()


class StageplanResourceHandler(BaseHandler):
    """
    URI: /api/stageplan/%project_number%/%stageplan_id%/
    VERBS: GET, PUT, DELETE

    Handles a single instance of StagePlan
    """

    allowed_methods = ('GET', 'PUT', 'DELETE')
    model = ProjectStage

    def read(self, request, project_number, stageplan_id):
        """ View a Project Stage """

        log.debug("GET request from user %s for project stage %s" % ( request.user, stageplan_id ))
        proj = Project.objects.get(project_number=project_number)
        stage = ProjectStage.objects.get(id=stageplan_id)

        if not check_project_read_acl(proj, request.user):
            log.debug("Refusing GET request for project %s from user %s" % ( project_number, request.user ))
            return rc.FORBIDDEN
        return stage

    def update(self, request, project_number, stageplan_id):
        """ Update the Project Stage """

        log.debug("PUT request from user %s for project stage %s" % ( request.user, stageplan_id))
        proj = Project.objects.get(project_number=project_number)
        stage = ProjectStage.objects.get(id=stageplan_id)
        log.debug("Fetched object from database %s" % stage)

        if not check_project_write_acl(proj, request.user):
            log.debug("Refusing PUT request for project %s from user %s" % ( project_number, request.user ))
            return rc.FORBIDDEN

        form = WBSProjectStage(request.POST, instance=stage)
        if form.is_valid():
            log.debug('Saving %s back to database' % t)
            t = form.save()
            return t
        else:
            resp = rc.BAD_REQUEST
            resp.write(form.errors)
            log.debug('Validation errors with %s' % t)
            return resp

    def delete(self, request, project_number, stageplan_id):
        """ Disassociate the stage from the project, not actually delete it """

        log.debug("DELETE request from user %s for project stage %s" % ( request.user, stageplan_id ))
        proj = Project.objects.get(project_number=project_number)
        stage = ProjectStage.objects.get(id=stageplan_id)
        log.debug("Fetched object from database %s" % stage)

        if not check_project_write_acl(proj, request.user):
            log.debug("Refusing DELETE request for project stage %s from user %s" % ( stageplan_id, request.user ))
            return rc.FORBIDDEN

        proj.stage_plan.remove(stage)
        proj.save()
        log.debug("Deleted project stage %s" % stage)
        return rc.ALL_OK


class EngineeringDayProjectListHandler(BaseHandler):
    """ 
    URL: /api/engineeringdays/%project_number%/
    VERBS: GET

    Returns a list of EngineeringDays associated with a project
    """

    allowed_methods = ('GET',)
    models = EngineeringDay

    def read(self, request, project_number):
        """ Return a list of project stages associated with projects filtered by ACL """

        log.debug("GET request from user %s for stage plan list" % request.user)
        proj = Project.objects.get(project_number=project_number)

        if not check_project_read_acl(proj, request.user):
            log.debug("Refusing GET request for project list %s from user %s" % ( project_number, request.user ))
            return rc.FORBIDDEN

        ret = []
        for stage in project.project_stages.all():
            for wbs in stage.work_items.all():
                ret += wbs.engineering_days.all()
        return ret



class EngineeringDayResourceHandler(BaseHandler):
    """
    URI: /api/engineeringday/%project_number%/%eday_id%/
    VERBS: GET, DELETE

    Handles a single instance of EngineeringDay
    """

    allowed_methods = ('GET', 'DELETE')
    model = EngineeringDay

    def read(self, request, project_number, eday_id):
        """ View an Engineering Day """

        log.debug("GET request from user %s for engineering day %s" % ( request.user, eday_id ))
        proj = Project.objects.get(project_number=project_number)
        eday = EngineeringDay.objects.get(id=eday_id)

        if not check_project_read_acl(proj, request.user):
            log.debug("Refusing GET request for project %s from user %s" % ( project_number, request.user ))
            return rc.FORBIDDEN
        return eday


    def delete(self, request, project_number, eday_id):
        """ Disassociate the day from the project, not actually delete it """

        log.debug("DELETE request from user %s for engineering day %s" % ( request.user, eday_id ))
        proj = Project.objects.get(project_number=project_number)
        stage = ProjectStage.objects.get(id=stageplan_id)
        log.debug("Fetched object from database %s" % stage)

        if not check_project_write_acl(proj, request.user):
            log.debug("Refusing DELETE request for project stage %s from user %s" % ( stageplan_id, request.user ))
            return rc.FORBIDDEN

        proj.stage_plan.remove(stage)
        proj.save()
        log.debug("Deleted project stage %s" % stage)
        return rc.ALL_OK


class EngineeringDayProjectListHandler(BaseHandler):
    """ 
    URL: /api/engineeringdays/%project_number%/
    VERBS: GET

    Returns a list of EngineeringDays associated with a project
    """

    allowed_methods = ('GET',)
    models = EngineeringDay

    def read(self, request, project_number):
        """ Return a list of engineering days associated with projects filtered by ACL """

        log.debug("GET request from user %s for eday list" % request.user)
        proj = Project.objects.get(project_number=project_number)

        if not check_project_read_acl(proj, request.user):
            log.debug("Refusing GET request for project list %s from user %s" % ( project_number, request.user ))
            return rc.FORBIDDEN

        return EngineeringDays.objects.filter(work_items__project_stage__project=proj)

class EngineeringDayWBSListHandler(BaseHandler):
    """ 
    URL: /api/engineeringdays/%project_number%/%wbs_id%/
    VERBS: GET, POST

    Returns a list of EngineeringDays associated with a Work Item, also
    adds a new EngineeringDay to the WorkItem
    """

    allowed_methods = ('GET', 'POST')
    models = EngineeringDay

    def read(self, request, project_number):
        """ Return a list of engineering days associated with a work item """

        log.debug("GET request from user %s for stage plan list" % request.user)
        proj = Project.objects.get(project_number=project_number)
        wbs = WorkItem.objects.get(id=wbs_id)

        if not check_project_read_acl(proj, request.user):
            log.debug("Refusing GET request for project list %s from user %s" % ( project_number, request.user ))
            return rc.FORBIDDEN

        return wbs.engineering_days.all()

    @validate(EngineeringDayForm)
    def create(self, request, project_number, wbs_id):
        """ Create a new Engineering Day """

        log.debug("POST request from user %s to create a new engineering day" % request.user)
        proj = Project.objects.get(project_number=project_number)

        if not check_project_write_acl(proj, request.user):
            log.debug("Refusing POST request for project %s from user %s" % ( project_number, request.user ))
            return rc.FORBIDDEN

        # Go ahead and create the engineering day....
        form = EngineeringDayForm(request.POST)
        t = form.save()
        wbs.engineering_days.add(t)
        wbs.save()
        return t

class EngineeringDayResourceFinderHandler(BaseHandler):
    """
    URI: /api/engineeringdays/%project_number%/%wbs_id%/resources/
    VERBS: GET

    Return a list of resources that are matched based on skillset to a Work Item
    """

    allowed_methods  = ('GET',)
    models = EngineeringDay

    def read(self, request, project_number, wbs_id):
        """ Return a list of resources able to work on a Work item """
        proj = Project.objects.get(project_number=project_number)
        if not check_project_read_acl(proj, request.user):
            log.debug("Refusing GET request for project %s from user %s" % ( project_number, request.user ))
            return rc.FORBIDDEN

        work_item = WorkItem.objects.get(id=wbs_id)
        requested_date = datetime.date(int(year), int(month), int(day))
        
        ret = [ ]
        
        resources = UserProfile.objects.filter(skillset=work_item.skill_set, user__is_active=True).order_by('user__first_name')
        log.debug('''Potential resources: %s.''' % resources)
        for res in resources:
                # Get the resources name
                if res.user.get_full_name() != '':
                        res_full_name = res.user.get_full_name()
                else:
                        res_full_name = res.user.username

                logging.debug('''Searching for Engineering days: work_date=%s, resource=%s, resource_id=%s''' % ( requested_date, res_full_name, res.user.id ))
                

                res_activity = EngineeringDay.objects.filter(work_date=requested_date, resource=res.user)

                r = {"pk": res.user.id }

                if len(res_activity) == 0: # Resource isn't booked at all
                        r['resource'] = '''%s - Available all day''' % res_full_name
                        r['available'] = True
                        logging.debug('''%s has no Engineering Days booked.''' % res)
                
                elif len(res_activity) >= 2: # User already has 2 bookings for this day
                        r['resource'] = '''%s - Booked out all day''' % res_full_name
                        r['available'] = False
                        logging.debug('''%s has 2 Engineering Days booked: %s.''' % ( res, res_activity ))
                else:
                        for day in res_activity:
                                if day.day_type == 0:
                                        r['resource'] = '''%s - Available PM only''' % res_full_name
                                        r['available'] = True
                                        logging.debug('''%s is available in PM. Booked on %s in AM.''' % ( res, day ))
                                elif day.day_type == 1:
                                        r['resource'] = '''%s - Available AM only''' % res_full_name
                                        r['available'] = True
                                        logging.debug('''%s is available in AM. Booked on %s in PM.''' % ( res, day ))
                                elif day.day_type == 2:
                                        r['resource'] = '''%s - Booked out all day''' % res_full_name
                                        r['available'] = False
                                        logging.debug('''%s has no availability. Booked on %s.''' % ( res, day ))


                try:
                        rota = RotaItem.objects.get(person=res.user, date=requested_date)
                        if rota.activity.unavailable_for_projects:
                                r['resource'] = '''%s - Not Available''' % res_full_name
                                r['available'] = False
                                logging.debug('''%s has no availability. Rota'd on %s.''' % ( res, rota ))
                except RotaItem.DoesNotExist:
                        pass
                                
                
                ret.append(r)
        return ret


class UserEngineeringDayListHandler(BaseHandler):
    """ 
    URI: /api/engineeringdays/
    VERBS: GET

    Returns a list of engineering days associated with an user
    """

    allowed_methods  = ('GET',)
    models = EngineeringDay

    def read(self, request, project_number, wbs_id):
        """ Return a list of engineering days associated with projects filtered by ACL """

        log.debug("GET request from user %s for engineering day list" % request.user)
        projects = Project.objects.filter(active=True, read_acl__in=request.user.groups.all()).exclude(project_status=5).distinct()
        return EngineeringDay.objects.filter(work_items__project_stage__project__in=projects).filter(resource=request.user)
        
        
class SkillsetListHandler(BaseHandler):
    """
    URL: /api/skillsets/
    VERBS: GET

    Return a skillsets configured in the tool
    """

    allowed_methods = ('GET',)

    def read(self, request):
        log.debug("GET request from user %s for skillsets" % request.user)
        return SkillSet.objects.all()

                

