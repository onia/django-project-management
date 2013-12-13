from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class RotaActivity(models.Model):

        activity = models.CharField('Activity', max_length=255)
        description = models.TextField('Description', blank=True)
        unavailable_for_projects = models.BooleanField('Unavailable for Project', default=False)
        active = models.BooleanField('Active', default=True)

        def __str__(self):
                return '''%s''' % self.activity

        class Meta:
                ordering = ('activity',)

class RotaItem(models.Model):

        date = models.DateField('Date')
        person = models.ForeignKey(User, related_name='rota_item')
        activity = models.ForeignKey(RotaActivity, verbose_name='Activity', related_name='rota_items')
        description = models.TextField('Description', blank=True)

        author = models.ForeignKey(User, related_name='rota_items_authored')
        created_date = models.DateTimeField(auto_now_add=True)
        modified_date = models.DateTimeField(auto_now=True)

        class Meta:
                permissions = (
                                ('can_edit', 'Can Edit Rota'),
                )

        def __str__(self):
                return '''%s - %s - %s''' % ( self.date.strftime("%Y-%m-%d"), self.person.username, self.activity.activity )

        

class Team(models.Model):

        name = models.CharField('Name', max_length=255) 
        members = models.ManyToManyField(User, verbose_name='Members', related_name='teams', blank=True, null=True)
        

        def __str__(self):
                return '''%s''' % self.name


