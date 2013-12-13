from django import template
from risks.models import Risk
from risks.forms import RiskForm

register = template.Library()


def get_risk_form(risk):

	try:
		r = Risk.objects.get(risk_number=risk)
	except Risk.DoesNotExist:
		return ''
	f = RiskForm(instance=r)
	return f.as_table()

register.simple_tag(get_risk_form)
	
