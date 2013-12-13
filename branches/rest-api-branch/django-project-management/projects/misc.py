import simplejson as json

from django.contrib.auth.models import *
from django.http import Http404

from projects.models import Company

def all_username_options():
        
        all_users = User.objects.filter(is_active=True).order_by('first_name')
        ret = [('', '------') ]
        for u in all_users:
                if u.get_full_name() == '':
                        uname = u.username
                else:
                        uname = u.get_full_name()
                ret.append( ( u.id, uname ) )
        return ret
        
def get_dependancies_for_project(project):

        ret = [('', '------') ]
        for wbs in project.work_items.all():
                ret.append( ( wbs.id, wbs.title ) )
        return ret

def get_resource_for_project(project):
        ret = [('', '------') ]
        all_users = User.objects.filter(is_active=True).order_by('first_name')
        for u in all_users:
                if u.get_full_name() == '':
                        uname = u.username
                else:
                        uname = u.get_full_name()
                for group in u.groups.all():
                        if group in project.read_acl.all():
                                ret.append( ( u.id, uname ) )

        return ret
                                

def check_project_read_acl(project, user):
        allowed_access = False
        for group in project.read_acl.all():
                if group in user.groups.all():
                        allowed_access = True
        if not allowed_access:
                return False
        return True

def check_project_write_acl(project, user):
        allowed_access = False
        for group in project.write_acl.all():
                if group in user.groups.all():
                        allowed_access = True
        if not allowed_access:
                return False
        return True

def all_company_options():
        ret = [('', '------') ]
        for c in Company.objects.filter(active=True):
                ret.append( ( c.id, c.company_name ) )
        return ret

def get_wip_assignee_list(wip_report):
        ret = [('', '------') ]
        for u in User.objects.filter(is_active=True).order_by('username'):
                if u.get_full_name() == '':
                        uname = u.username
                else:
                        uname = u.get_full_name()
                for g in wip_report.read_acl.all():
                        if g in u.groups.all():
                                if ( ( u.id, uname ) ) not in ret:
                                        ret.append( ( u.id, uname ) )
                        
        return ret      

        
def handle_form_errors(error_dict):
        errors =  dict([(k, [unicode(e) for e in v]) for k,v in error_dict.items()])
        ret = { "success": False, "errors": errors, "errormsg": "Sorry, there was an error with your submission" }
        return json.dumps(ret)
        
def return_json_success():
        ret = {"success": True}
        return json.dumps(ret)

def handle_generic_error(error_msg):
        ret = { "success": False, "errormsg": error_msg }
        return json.dumps(ret)
        
def user_has_write_access(project, user):
        for g in user.groups.all():
                if g in project.write_acl.all():
                        return True
        return False
        
