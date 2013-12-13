from django.contrib.auth.models import *
from projects.models import *
import settings

def getReadProjectList(request):

        l = []
        for group in settings.CORE_PROJECT_MANAGERS:
                g = Group.objects.get(name__exact=group)
                if g in request.user.groups.all():
                        for project in Project.objects.filter(active=True).exclude(projectStatus__exact='Archived'):
                                l.append(project.id)
                        return l

        for project in Project.objects.filter(active=True).exclude(projectStatus__exact='Archived'):
                for readGroup in project.readACL.all():
                        if readGroup in request.user.groups.all():
                                l.append(project.id)

        return l
                                
