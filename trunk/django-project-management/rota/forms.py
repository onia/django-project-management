from django.forms import *
from django.contrib.admin import widgets                                       
from rota.models import *


class EditRotaForm(Form):
        
        monday = IntegerField(required=False)
        monday_description = CharField(max_length=1024, required=False)
        tuesday = IntegerField(required=False)
        tuesday_description = CharField(max_length=1024, required=False)
        wednesday = IntegerField(required=False)
        wednesday_description = CharField(max_length=1024, required=False)
        thursday = IntegerField(required=False)
        thursday_description = CharField(max_length=1024, required=False)
        friday = IntegerField(required=False)
        friday_description = CharField(max_length=1024, required=False)
        saturday = IntegerField(required=False)
        saturday_description = CharField(max_length=1024, required=False)
        sunday = IntegerField(required=False)
        sunday_description = CharField(max_length=1024, required=False)
        monday_date = CharField(max_length=255)
        person_id = IntegerField(required=False)
