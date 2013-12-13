import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.html import linebreaks

# Create your models here.
class SkillSet(models.Model):

        skill = models.CharField('Skill', max_length=255)
        #project_resources = models.ManyToManyField(User, verbose_name='Resources with this skill', related_name='project_skill', null=True, blank=True)

        def __str__(self):
                return self.skill

class ProjectStage(models.Model):

        stage = models.CharField('Project Stage', max_length=255)
        description = models.TextField()
        stage_number = models.IntegerField()
        
        def __str__(self):
                return self.stage

        class Meta:
                ordering = ['stage_number']

class EngineeringDay(models.Model):

        DAY_LENGTH = (
                                (0, 'Half-day AM'),
                                (1, 'Half-day PM'),
                                (2, 'Full Day'),
        )

        work_date = models.DateField('Work Date')
        resource = models.ForeignKey(User, verbose_name='Engineering Resource')
        history = models.TextField('History', blank=True)       
        day_type = models.IntegerField('Work Units', choices=DAY_LENGTH)

        created_date = models.DateTimeField(auto_now_add=True)
        modified_date = models.DateTimeField(auto_now=True)
        
        
        def __str__(self):
                return '''%s - %s - %s''' % ( self.id, self.work_date.strftime("%Y-%m-%d"), self.resource.username )
        
        def get_absolute_url(self):
                if self.work_item.all() != []:  # If the EngineeringDay is referenced by a WorkItem...
                        try:
                                return '''/WBS/%s/Edit/#%s''' % ( self.work_item.all()[0].project.all()[0].project_number, self.id )
                        except: 
                                return ''
                elif self.wip_item.all() != []: # If the EngineeringDay is referenced by a WIPItem...
                        try:
                                return '''%s#work_item_%s''' % ( self.wip_item.all()[0].heading.all()[0].report.all()[0].get_absolute_url(), self.wip_item.all()[0].id )
                        except:
                                return ''
        

        def find_suitable_resource(self, day):
        
                ''' Find a User with the right skillset that is available on this day '''

                potential_users = UserProfile.objects.filter()

class WorkItem(models.Model):

        created_date = models.DateTimeField(auto_now_add=True)
        modified_date = models.DateTimeField(auto_now=True)
        skill_set = models.ForeignKey(SkillSet, verbose_name='Skill set required')
        project_stage = models.ForeignKey(ProjectStage, verbose_name='Project Stage', related_name='work_items', blank=True, null=True)
        author = models.ForeignKey(User, related_name='authored_tasks')
        title = models.CharField('Title', max_length=255)
        description = models.TextField('Description')
        depends = models.ForeignKey('self', verbose_name='Depends', null=True, blank=True)
        duration = models.IntegerField('Duration of Task', null=True, blank=True)
        owner = models.ForeignKey(User, verbose_name='Owner', related_name='assigned_tasks')
        percent_complete = models.IntegerField('Percent complete', null=True, blank=True)
        active = models.BooleanField(default=True) 
        start_date = models.DateTimeField('Start Date', null=True, blank=True)
        finish_date = models.DateTimeField('Finish Date', null=True, blank=True)
        wbs_number = models.IntegerField('WBS Number', max_length=255, blank=True, null=True)
        cost = models.IntegerField('Cost', null=True, blank=True)
        history = models.TextField('Task History', blank=True)
        engineering_days = models.ManyToManyField(EngineeringDay, verbose_name="Engineering Days", related_name="work_item", blank=True, null=True)

        def __str__(self):
                return self.title

        def get_absolute_url(self):
                return '''/WBS/%s/Edit/#%s''' % ( self.project.all()[0].project_number, self.id )

        def get_work_item_status(self):
                now = datetime.datetime.now()                                                                           # now = datetime.datetime(2009, 9, 14, 17, 21, 29, 220270)
                today = datetime.date( now.year, now.month, now.day )
                status = ''

                if self.percent_complete < 100:
                        if self.finish_date:
                                # Is the task more than 5 days late?
                                diff = now - self.finish_date
                                if diff.days > 5:
                                        return 'rag_status_red'
                                elif diff.days > 4 and diff.days > 0:
                                        return 'rag_status_amber'
                        return 'rag_status_white'
                else:
                        return 'rag_status_green'
        
        def get_history_html(self):
            return linebreaks(self.history)

        class Meta:
                ordering = ['wbs_number']

