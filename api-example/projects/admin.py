from projects.models import *
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class ProjectAdmin(admin.ModelAdmin):

        fieldsets = ( 
                        (None, { 'fields': ('project_name', 'project_status', 'company', 'project_manager', 'project_number', 'duration_type', 'project_sponsor', 'read_acl', 'write_acl') }),

        )

        list_display = ['project_name', 'project_status', 'company', 'project_number']
        search_fields = ['project_number', 'project_description']
                        

admin.site.register(Project, ProjectAdmin)
admin.site.register(Company)
admin.site.register(ServiceAccount)

admin.site.unregister(User)

# Set it up so we can edit a user's sprockets inline in the admin
class UserProfileInline(admin.StackedInline):
        model = UserProfile

class MyUserAdmin(UserAdmin):
        inlines = [UserProfileInline]

# re-register the User with the extended admin options
admin.site.register(User, MyUserAdmin)

