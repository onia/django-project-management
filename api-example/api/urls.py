from django.conf.urls.defaults import *
from piston.authentication import HttpBasicAuthentication
from piston.resource import Resource
from api.emitters import *
from api.authentication import DjangoAuthentication
from projects.api_views import ProjectResourceHandler, ProjectListHandler, CompanyListHandler, \
        TeamManagersListHandler, NonTeamManagersListHandler, ResourcesListHandler
from deliverables.api_views import DeliverableResourceHandler, DeliverableListHandler 
from risks.api_views import RiskResourceHandler, RiskListHandler, \
        UserRiskListHandler
from wbs.api_views import WBSResourceHandler, WBSListHandler, \
        UserWBSListHandler, StageplanResourceHandler, \
        StageplanListHandler, EngineeringDayResourceHandler, \
        EngineeringDayWBSListHandler, EngineeringDayProjectListHandler, \
        UserEngineeringDayListHandler, EngineeringDayResourceFinderHandler, \
        SkillsetListHandler
from lessons.api_views import LessonResourceHandler, LessonListHandler 


auth = DjangoAuthentication()
ad = { 'authentication': auth }

# Handlers defined in projects.api_views
team_managers_handler = Resource(TeamManagersListHandler, **ad)
non_team_managers_handler = Resource(NonTeamManagersListHandler, **ad)
resources_handler = Resource(ResourcesListHandler, **ad)
project_handler = Resource(ProjectResourceHandler, **ad)
project_list_handler = Resource(ProjectListHandler, **ad)
company_list_handler = Resource(CompanyListHandler, **ad)

# Handlers defined in risks.api_views
risk_handler = Resource(RiskResourceHandler, **ad)
risk_list_handler = Resource(RiskListHandler, **ad)
user_risk_list_handler = Resource(UserRiskListHandler, **ad)

# Handlers defined in deliverables.api_views
deliverable_handler = Resource(DeliverableResourceHandler, **ad)
deliverable_list_handler = Resource(DeliverableListHandler, **ad)

# Handlers defined in lessons.api_views
lesson_handler = Resource(LessonResourceHandler, **ad)
lesson_list_handler = Resource(LessonListHandler, **ad)

# Handlers defined in wbs.api_views
skillset_list_handler = Resource(SkillsetListHandler, **ad)
wbs_handler = Resource(WBSResourceHandler, **ad)
wbs_list_handler = Resource(WBSListHandler, **ad)
#wbs_reorder_handler = Resource(WBSReorderHandler, **ad)
user_wbs_list_handler = Resource(UserWBSListHandler, **ad)

stageplan_handler = Resource(StageplanResourceHandler, **ad)
stageplan_list_handler = Resource(StageplanListHandler, **ad)

engineeringday_handler = Resource(EngineeringDayResourceHandler, **ad)
engineeringday_project_list_handler = Resource(EngineeringDayProjectListHandler, **ad)
engineeringday_wbs_list_handler = Resource(EngineeringDayWBSListHandler, **ad)
engineeringday_resource_handler = Resource(EngineeringDayResourceFinderHandler, **ad)
user_engineeringday_list_handler = Resource(UserEngineeringDayListHandler, **ad)

urlpatterns = patterns('',
    # URLs handled in projects.api_views
    (r'projects/(?P<project_number>[-\w\./\s]+)/team_managers/$', team_managers_handler),
    (r'projects/(?P<project_number>[-\w\./\s]+)/non_team_managers/$', non_team_managers_handler),
    (r'projects/(?P<project_number>[-\w\./\s]+)/resources/$', resources_handler),
    (r'projects/(?P<project_number>[-\w\./\s]+)/$', project_handler),
    (r'projects/$', project_list_handler),
    (r'companies/$', company_list_handler),
    (r'skillsets/$', skillset_list_handler),

    # URLs handled in risks.api_views
    (r'risks/(?P<project_number>[-\w\./\s]+)/(?P<risk_number>[-\w\./\s]+)/$', risk_handler),
    (r'risks/(?P<project_number>[-\w\./\s]+)/$', risk_list_handler),
    (r'risks/$', user_risk_list_handler),

    # URLs handled in deliverables.api_views
    (r'deliverables/(?P<project_number>[-\w\./\s]+)/(?P<deliverable_id>[-\w\./\s]+)/$', deliverable_handler),
    (r'deliverables/(?P<project_number>[-\w\./\s]+)/$', deliverable_list_handler),

    # URLs handled in lessons.api_views
    (r'lessons/(?P<project_number>[-\w\./\s]+)/(?P<lesson_id>[-\w\./\s]+)/$', lesson_handler),
    (r'lessons/(?P<project_number>[-\w\./\s]+)/$', lesson_list_handler),

    # URLs handled in wbs.api_views
    (r'wbs/(?P<project_number>[-\w\./\s]+)/(?P<wbs_id>[-\w\./\s]+)/$', wbs_handler),
    (r'wbs/(?P<project_number>[-\w\./\s]+)/$', wbs_list_handler),
    #(r'wbs/(?P<project_number>[-\w\./\s]+)/reorder/$', wbs_reorder_handler),
    (r'wbs/$', user_wbs_list_handler),

    (r'stageplan/(?P<project_number>[-\w\./\s]+)/(?P<stageplan_id>[-\w\./\s]+)/$', stageplan_handler),
    (r'stageplan/(?P<project_number>[-\w\./\s]+)/$', stageplan_list_handler),

    (r'engineeringdays/(?P<project_number>[-\w\./\s]+)/$', engineeringday_project_list_handler),
    (r'engineeringdays/(?P<project_number>[-\w\./\s]+)/(?P<wbs_id>[-\w\./\s]+)$', engineeringday_wbs_list_handler),
    (r'engineeringdays/(?P<project_number>[-\w\./\s]+)/(?P<eday_id>[-\w\./\s]+)/$', engineeringday_handler),
    (r'resources/(?P<project_number>[-\w\./\s]+)/(?P<wbs_id>[-\w\./\s]+)/resources/$', engineeringday_resource_handler),
    (r'engineeringdays/$', user_engineeringday_list_handler),

)
