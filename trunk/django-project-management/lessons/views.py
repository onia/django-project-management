# Create your views here.
import simplejson as json

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, Template, RequestContext
from django.template.loader import get_template
from django.template.defaultfilters import slugify
from django.shortcuts import render_to_response
from django.db.models import Q
from projects.models import *
from projects.views import updateLog
from lessons.forms import *
from projects.misc import handle_form_errors, check_project_read_acl, check_project_write_acl, return_json_success, handle_generic_error


@login_required
def add_lesson(request, project_number):

        project = Project.objects.get(project_number=project_number)
        lessons = LessonLearnt.objects.filter(project=project)
        if request.method == 'POST':
                form = LessonForm(request.POST)
                if form.is_valid():
                        t = form.save()
                        t.save()
                        project.lessons_learnt.add(t)
                        project.save()
                        request.user.message_set.create(message='''Lesson %s Registered''' % t.id)
                        updateLog(request, project_number, '''Lesson %s Registered''' % t.id)
                        return HttpResponse( return_json_success() )
                else:
                        return HttpResponse( handle_form_errors(form.errors))

@login_required
def edit_lesson(request, project_number, lesson_id):

        project = Project.objects.get(project_number=project_number)
        lesson = LessonLearnt.objects.get(id=lesson_id)
        if request.method == 'POST':
                form = LessonForm(request.POST, instance=lesson)
                if form.is_valid():
                        t = form.save()
                        t.save()
                        request.user.message_set.create(message='''Lesson %s Edited''' % t.id)
                        for change in form.changed_data:
                                updateLog(request, project_number, '%s changed to %s' % ( change, eval('''t.%s''' % change)))
                        return HttpResponse( return_json_success() )
                else:
                        return HttpResponse( handle_form_errors(form.errors))


@login_required
def delete_lesson(request, project_number, lesson_id):

        project = Project.objects.get(project_number=project_number)
        try:
                lesson = LessonLearnt.objects.get(id=lesson_id)
        except Lesson.DoesNotExist:
                return HttpResponse( handle_generic_error("Lesson does not exist"))
        project.lessons_learnt.remove(lesson)
        project.save()
        return HttpResponse( return_json_success() )
        
                        

                
@login_required
def view_lessons(request, project_number):
        project = Project.objects.get(project_number=project_number)
        check_project_read_acl(project, request.user)   # Will return Http404 if user isn't allowed to view project

        return HttpResponse( serializers.serialize('json', project.lessons_learnt.all(), relations={'author': {'fields': ('username',), 'extras': ('get_full_name',)}}))
        
@login_required
def view_lesson(request, project_number, lesson_id):
        project = Project.objects.get(project_number=project_number)
        check_project_read_acl(project, request.user)   # Will return Http404 if user isn't allowed to view project
        lesson = LessonLearnt.objects.get(id=lesson_id)

        JSONSerializer = serializers.get_serializer('json')
        j = JSONSerializer()
        j.serialize([lesson], fields=('description', 'publish_to_client'))
        
        return HttpResponse( '''{ success: true, data: %s }''' % json.dumps(j.objects[0]['fields']))
        
