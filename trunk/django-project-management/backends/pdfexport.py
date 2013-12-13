from django import http
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context
import ho.pisa as pisa
import cStringIO as StringIO
import cgi
import settings


def render_to_pdf(template_src, context_dict, filename="DJANGO-PROJECT-MANAGEMENT.pdf"):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result, path=settings.STATIC_DOC_ROOT)
    if not pdf.err:
        response =  http.HttpResponse(result.getvalue(), mimetype='application/pdf')
        response['Content-Disposition'] = 'attachment;filename=%s' % filename
        return response
    return http.HttpResponse('We had some errors<pre>%s</pre>' % cgi.escape(html))

def html_to_pdf(html, filename="DJANGO-PROJECT-MANAGEMENT.pdf"):
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result, path=settings.STATIC_DOC_ROOT)
    if not pdf.err:
        response =  http.HttpResponse(result.getvalue(), mimetype='application/pdf')
        response['Content-Disposition'] = 'attachment;filename=%s' % filename
        return response
    return http.HttpResponse('We had some errors<pre>%s</pre>' % cgi.escape(html))
        
        


