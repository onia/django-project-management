from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.html import urlize
from projects.models import Company
from wbs.models import EngineeringDay
from django.utils.html import linebreaks

# Create your models here.

                                
class WIPItem(models.Model):

        WIP_STATUS = (
                                (1, 'Active'),
                                (2, 'On Hold'),
        )

        created_date = models.DateTimeField(auto_now_add=True, verbose_name='Date Created')
        modified_date = models.DateTimeField(auto_now=True, verbose_name='Last Update')
        description = models.TextField('Description')
        assignee = models.ForeignKey(User, verbose_name='Assignee')
        history = models.TextField('History', blank=True)
        objective = models.BooleanField('Objective')
        deadline = models.DateField('Deadline', blank=True, null=True)
        status = models.IntegerField('Status', choices=WIP_STATUS, default=1)
        complete = models.BooleanField('Completed')
        engineering_days = models.ManyToManyField(EngineeringDay, verbose_name="Engineering Days", related_name="wip_item", blank=True, null=True)

        def get_absolute_url(self):
                return '''%s#work_item_%s''' % ( self.heading.all()[0].report.all()[0].get_absolute_url(), self.id )

        def get_ajax_form(self):
                return '''/WIP/AjaxLoadForm/%s/''' % self.id

        def get_heading(self):
                if self.heading.all() != '':
                        return '''%s - %s''' % ( self.heading.all()[0].company.company_name, self.heading.all()[0].heading )

        def get_engineering_days_as_ul(self):
                str = '''<ul>'''
                for e in self.engineering_days.all():
                        str += '''<li>%s - %s - %s</li>''' % ( e.work_date.strftime("%A %e %B %Y"), e.get_day_type_display(), e.resource.get_full_name() )      
                str += '''</ul>'''
                return str      

        def __str__(self):
                return self.description[:50]

        def get_history_html(self):
            return linebreaks(self.history)

class Heading(models.Model):

        company = models.ForeignKey(Company, verbose_name='Company')
        heading = models.CharField('Heading', max_length=255)
        wip_items = models.ManyToManyField(WIPItem, verbose_name='WIP Items', related_name='heading', blank=True, null=True)
        active = models.BooleanField('Active', default=True)

        def __str__(self):
                return self.heading

        def get_absolute_url(self):
                return '''%s#heading_%s''' % ( self.report.all()[0].get_absolute_url(), self.id )
        
        def get_heading(self):
                return '''%s - %s''' % ( self.company.company_name, self.heading )      

        class Meta:
                ordering = ('company',)

class WIPReport(models.Model):

        name = models.CharField('WIP Report', max_length=255, unique=True)
        read_acl = models.ManyToManyField(Group, verbose_name='Read ACL', related_name='read_wip_reports', null=True, blank=True)
        write_acl = models.ManyToManyField(Group, verbose_name='Write ACL', related_name='write_wip_reports', null=True, blank=True)
        active = models.BooleanField('Active', default=True)
        headings = models.ManyToManyField(Heading, verbose_name='Headings', related_name='report',  blank=True, null=True)
        agenda = models.TextField('Agenda', blank=True)
        any_other_business = models.TextField('AOB', blank=True)

        def __str__(self):
                return self.name

        def get_absolute_url(self):
                return '''/WIP/%s/''' % urlize(self.name)
        
        def get_download_url(self):
                return '''/WIP/Download/%s/''' % urlize(self.name)


class WIPArchive(models.Model):

        wip_report = models.ForeignKey(WIPReport, verbose_name='WIP Report', related_name='archives')
        created_date = models.DateField(auto_now_add=True)
        html = models.TextField('HTML Report')

        def __str__(self):
                return '''%s - %s''' % ( self.wip_report.name, self.created_date )

        def get_absolute_url(self):
                return '''/WIP/DownloadArchive/%s/''' % self.id
