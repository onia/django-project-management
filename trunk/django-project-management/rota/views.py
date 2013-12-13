# Create your views here.
import calendar
import datetime
import simplejson as json
import logging

from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import Context, Template, RequestContext
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.db.models import Q
from rota.models import RotaActivity, RotaItem, Team 
from rota.forms import EditRotaForm
from wbs.models import EngineeringDay
from backends.pdfexport import render_to_pdf
from projects.misc import handle_form_errors, check_project_read_acl, check_project_write_acl, return_json_success, handle_generic_error, user_has_write_access
import settings

@login_required
def view_users(request):
        return HttpResponse( serializers.serialize('json', User.objects.filter(is_active=True), fields=('id', 'username'), extras=('get_full_name')))

@login_required
def rota_homepage(request, rota_url):
        return render_to_response('rota/rota.html', {'rota_url': rota_url }, context_instance=RequestContext(request))
        
@login_required
def view_rota_activities(request):
        return HttpResponse( serializers.serialize('json', RotaActivity.objects.filter(active=True)))   

@login_required
def view_rota(request, year=False, month=False, day=False, template=False, pdf=False, scope=False):
        
        # No additional security required here apart from a valid login. We allow all users to view 
        # their own rota plus the team and department rotas, and if they know the Edit Rota URL (hidden by default) they 
        # can load that page but not actually do anything in rota.views.edit_rota()

        cal = calendar.Calendar()
        now = datetime.datetime.now()                                                                           # now = datetime.datetime(2009, 9, 14, 17, 21, 29, 220270)
        today = datetime.date( now.year, now.month, now.day )

        if year and month and day:
                # User has asked for a specific week to be shown
                requested = datetime.date(int(year), int(month), int(day))      
        else:
                # Work out the days for this week
                requested = today
                
        this_week = calculate_week(requested)

        # [ { 'user': 'smorris', 'pk': '1', 'monday_rota': 'Infrastructure Mid', 'monday_eday': 'Free', 'tuesday_rota'
        ret = []

        logging.debug('''Requesting rota with scope => %s''' % ( scope ))

        if scope == 'all':
                scope_users = User.objects.filter(is_active=True).order_by('first_name').distinct()
        elif scope == 'team':
                scope_users = User.objects.filter(teams__in=request.user.teams.all(), is_active=True).order_by('first_name').distinct()
        else:
                scope_users = User.objects.filter(id=request.user.id)

        for u in scope_users:
                logging.debug('''Getting rota for %s''' % u)
                x = {'user': u.get_full_name(), 'pk': u.id }
                for day in this_week:
                        try:
                                _rota_item = RotaItem.objects.get(person=u, date=day)
                                #logging.debug('''%s has %s as a rota item''' % ( u, _rota_item )
                                summary = '''%s''' % _rota_item.activity
                                rotaitem = '''%s''' % _rota_item.activity
                                rotaitem_description = '''%s''' % _rota_item.description
                        
                                logging.debug('''Found existing rota item for %s: %s''' % ( u, summary ))
                        except RotaItem.DoesNotExist:
                                summary = ''
                                rotaitem = ''
                                rotaitem_description = ''

                        # Include engineering day information in the rota
                        _engineering_days = EngineeringDay.objects.filter(work_date=day, resource=u).distinct()
                        edays = ''
                        for d in _engineering_days:
                                if d.wip_item.all():
                                        summary += '''<br>(%s) WIP Item''' % ( d.get_day_type_display() )
                                        edays += '''<br>(%s) %s''' % ( d.get_day_type_display(), d.wip_item.all()[0].description )      
                                elif d.work_item.all():
                                        summary += '''<br>(%s) Project Work''' % ( d.get_day_type_display() )
                                        edays += '''<br>(%s) %s''' % ( d.get_day_type_display(), d.work_item.all()[0].title )   
                                else:
                                        pass
                
                        x['''%s_s''' % day.isoweekday()] = str(summary)
                        x['''%s_eday''' % day.isoweekday()] = str(edays)
                        x['''%s_r''' % day.isoweekday()] = str(rotaitem)
                        x['''%s_r_d''' % day.isoweekday()] = str(rotaitem_description)
                        x['monday_date'] = str(this_week[0])
                                
                ret.append(x)

                        
        return HttpResponse(json.dumps(ret))

@login_required
def edit_rota(request):

        # Some security, if the user isn't allowed to edit the rota raise 404
        if not request.user.has_perm('rota.can_edit'):
                raise Http404

        form = EditRotaForm(request.POST)       
        if form.is_valid():
                c = form.cleaned_data
                user = User.objects.get(id=c['person_id'])
                requested_week = calculate_week(datetime.datetime.strptime(c['monday_date'], "%Y-%m-%d"))
                
                #Get the existing Rota objects if they exist and edit or create them
                days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
                
                for d in range(0,7):
                        # No point proceeding with this day if there isn't a rota item to create
                        if c[days[d]]:
                                try:
                                        r = RotaItem.objects.get(person=user, date=requested_week[d])
                                except RotaItem.DoesNotExist:
                                        r = RotaItem()
                                r.person = user
                                r.date = requested_week[d]
                                r.activity = RotaActivity.objects.get(id=c[days[d]])
                                r.description = c['%s_description' % days[d]]
                                r.author = request.user
                                r.save()
                                logging.debug('''Added rota item... user=>%s, date=>%s, activity=>%s''' % ( r.person, r.date, r.activity ))

                return HttpResponse( return_json_success() )
        else:
                return HttpResponse( handle_form_errors(form.errors))
                
        

def calculate_week(requested_date):

        ''' Returns a list of days - this_week - given a date. '''

        cal = calendar.Calendar()
        day_of_week = calendar.weekday( requested_date.year, requested_date.month, requested_date.day )                                         # 0 = Monday, 1 = Tuesday, 2 = Wednesday
        monday_of_this_week = requested_date + datetime.timedelta(days=-day_of_week)                                                                            # datetime.datetime(2009, 9, 14, 17, 21, 29, 220270)
        monday_of_this_week = datetime.date( monday_of_this_week.year, monday_of_this_week.month, monday_of_this_week.day )     # Abbreviate down to one day
        
        for week in cal.monthdatescalendar( requested_date.year, requested_date.month ):
                if monday_of_this_week in week:
                        return week

def get_rota_for_user(request, user_id, date):
        user = User.objects.get(id=user_id)
        requested_week = calculate_week( datetime.datetime.strptime(date, "%Y-%m-%d"))

        rota_items = RotaItem.objects.filter(date__gt=requested_week[0]-datetime.timedelta(days=1), date__lt=requested_week[-1]-datetime.timedelta(days=-1), person=user)
        
        ret = {}
        ret['success'] = True
        ret['data'] = {}
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        for d in range(0,7):
                x = rota_items.filter(date=requested_week[d])   
                if x:
                        ret['data'][days[d]] = x[0].activity.id
                        ret['data']['''%s_description''' % days[d]] = x[0].description
                else:
                        ret['data'][days[d]] = ''
                        ret['data']['''%s_description''' % days[d]] = ''

        return HttpResponse( json.dumps(ret))
                
        

