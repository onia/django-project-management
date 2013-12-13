from django import template
from lessons.models import LessonLearnt
from lessons.forms import LessonForm

register = template.Library()


def get_lesson_form(lesson):

	try:
		r = LessonLearnt.objects.get(id=lesson)
	except LessonLearnt.DoesNotExist:
		return ''
	f = LessonForm(instance=r)
	return f.as_table()

register.simple_tag(get_lesson_form)
	
