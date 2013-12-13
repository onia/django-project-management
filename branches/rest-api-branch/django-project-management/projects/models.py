from django.db import models
from django.contrib.auth.models import User, Group
from lessons.models import LessonLearnt
from risks.models import Risk
from wbs.models import WorkItem, SkillSet, ProjectStage
from issues.models import Issue
from deliverables.models import Deliverable
from change_management.models import RequestForChange
from files.models import ProjectFile
from rota.models import Team


# Create your models here.

class ServiceAccount(models.Model):

    realm = models.CharField(max_length=255)
    bind_dn = models.CharField(max_length=1024)
    bind_pw = models.CharField(max_length=1024)
    base_dn = models.CharField(max_length=1024)
    ldap_servers = models.CharField(max_length=1024)
    active = models.BooleanField(default=True)
    priority = models.CharField(max_length=1024)

    def __str__(self):
        return self.realm

    class Meta:
        ordering = ('priority',)

class Company(models.Model):

    company_name = models.CharField(max_length=255, unique=True)
    active = models.BooleanField(default=True)
    logo = models.FileField(blank=True, upload_to="company_logos")

    class Meta:
        ordering = ('company_name',)

    def __str__(self):
        return self.company_name

class ExecutiveSummary(models.Model):

    TYPES = (
        (1, 'Checkpoint Report'),
        (2, 'Executive Summary'),
    )

    author = models.ForeignKey(User, verbose_name='Author')
    type = models.IntegerField('Type', choices=TYPES)
    summary = models.TextField('Summary')   
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '''%s''' % self.summary[:50]

    class Meta:
        ordering = ('-created_date',)

class Project(models.Model):

    PROJECT_STATUS = (      
        (0, 'Proposed'),
        (1, 'Draft'),
        (2, 'Active'),
        (3, 'On hold'),
        (4, 'Completed'),
        (5, 'Archived'),
        (6, 'Informational'),
    )

    DURATION_TYPE = (
        (0, 'Hours'),
        (1, 'Days'),
    )

    ''' Django object to describe a Project and relationships to all it's other data '''

    project_name = models.CharField(max_length=255, unique=True, help_text='''Choose a short name for the project''')
    project_status = models.IntegerField(max_length=255, choices=PROJECT_STATUS)
    company = models.ForeignKey(Company)
    project_manager = models.ForeignKey(User, related_name='project_manager')
    team_managers = models.ManyToManyField(User, null=True, blank=True, related_name='project_team_managers')
    project_number = models.CharField(max_length=255, unique=True)
    project_sponsor = models.CharField('Project Sponsor', max_length=255)
    project_description = models.CharField(max_length=1024)
    business_case = models.TextField(max_length=10240, blank=True)
    business_benefits = models.TextField(max_length=10240, blank=True)
    project_scope = models.TextField(max_length=10240, blank=True)
    exclusions = models.TextField(max_length=10240, blank=True)
    assumptions = models.TextField(max_length=10240, blank=True)
    quality_plan = models.TextField(max_length=10240, blank=True)
    communications_plan = models.TextField(max_length=10240, blank=True)
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    attached_files = models.FileField(upload_to='project_files', blank=True)
    read_acl = models.ManyToManyField(Group, null=True, blank=True, related_name='project_readacl') 
    write_acl = models.ManyToManyField(Group, null=True, blank=True, related_name='project_writeacl')       
    deliverables = models.ManyToManyField(Deliverable, null=True, blank=True, related_name='project')
    risks = models.ManyToManyField(Risk, null=True, blank=True, related_name='project')
    issues = models.ManyToManyField(Issue, null=True, blank=True, related_name='project')
    lessons_learnt = models.ManyToManyField(LessonLearnt, null=True, blank=True, related_name='project')
    rfpc = models.ManyToManyField(RequestForChange, null=True, blank=True, related_name='project')
    work_items = models.ManyToManyField(WorkItem, null=True, blank=True, related_name='project')
    files = models.ManyToManyField(ProjectFile, null=True, blank=True, related_name='project_files')
    work_item_order = models.CharField('Order of Work Items', max_length=1024, blank=True)
    executive_summary = models.ManyToManyField(ExecutiveSummary, blank=True, null=True, related_name='project')
    stage_plan = models.ManyToManyField(ProjectStage, blank=True, null=True, related_name='project')
    duration_type = models.IntegerField(choices=DURATION_TYPE)


    def __str__(self):
        return self.project_name

    def get_absolute_url(self):
        return '''/Projects/%s/''' % self.project_number

    class Meta:
        permissions = (
            ('can_change_status', 'Can Change Status of Project'),
            ('can_create_project', 'Can Create Project'),
            ('can_view_rota_link', 'Can View Rota Link'),
            ('can_view_wip_link', 'Can View WIP Link'),
        )
        
        ordering = ['project_number']

class HistoryLog(models.Model):

    project = models.ForeignKey(Project, related_name='project_historyLog')
    user = models.ForeignKey(User, related_name='user_historyLog')
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=1024)

    def __str__(self):
        return '''%s %s''' % ( self.user, self.date )

class UserProfile(models.Model):

    user = models.ForeignKey(User, unique=True)
    skillset = models.ManyToManyField(SkillSet, verbose_name='Skillset', related_name='resources',  blank=True, null=True)
                
        
