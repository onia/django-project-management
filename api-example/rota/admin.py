from rota.models import *
from django.contrib import admin


class RotaActivityAdmin(admin.ModelAdmin):

        list_display = ['activity', 'description', 'unavailable_for_projects', 'active']
        search_fields = ['description', 'activity']


admin.site.register(RotaActivity, RotaActivityAdmin)
#admin.site.register(RotaItem)
admin.site.register(Team)

