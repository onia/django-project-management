import re

from django.db.models import Q
from django.http import Http404, HttpResponseRedirect, HttpResponse, HttpResponsePermanentRedirect
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext, Template, loader, TemplateDoesNotExist
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.views import redirect_to_login
from django.utils import translation, simplejson
from django.utils.translation import ugettext as _, check_for_language
from django.utils.encoding import smart_unicode, iri_to_uri

from cms.forms import SearchForm
from cms.models import Page, RootPageDoesNotExist
from cms.util import PositionDict, language_list, resolve_dotted_path
from cms.cms_global_settings import *

def get_page_context(request, language, page, extra_context={}):
    context = RequestContext(request)
    path = list(page.get_path())

    try:
        page_number = int(request.GET.get('page'))
    except (TypeError, ValueError):
        page_number = 1

    context.update({
        'page': page,
        'page_number': page_number,
        'path': path,
        'language': language,
        'root':'/%s/' % language,
        'site_title': SITE_TITLE,
    })
    context.update(extra_context)
    return context

def render_pagecontent(page_content, context):
    # Parse template tags
    if page_content.allow_template_tags:
        template = Template(
                '{%% load i18n cms_base cms_extras %s %%}'
                '{%% cms_pagination %d %%}%s{%% cms_end_pagination %%}' % (
                    ' '.join(TEMPLATETAGS),
                    context['page_number'],
                    page_content.content
                )
            )
        content = template.render(context)
    else:
        content = page_content.content

    return page_content.title, content


def render_page(request, language, page, template_name=None, preview=None, args=None):
    """
    Renders a page in the given language.

    A template_name can be given to override the default page template.
    A PageContent object can be passed as a preview.
    """
    # if the given page requires login but the user is not authenticated
    if page.requires_login and not request.user.is_authenticated():
        return redirect_to_login(next=page.get_absolute_url())

    # if there is no published root page
    if not Page.objects.root().published(request.user) or not page.published(request.user):
        raise Http404

    # Make translations using Django's i18n work
    translation.activate(language)
    request.LANGUAGE_CODE = translation.get_language()

    # Initialize content/title dicts.
    content_dict = PositionDict(POSITIONS[0][0])
    title_dict = PositionDict(POSITIONS[0][0])

    context = get_page_context(request, language, page)

    # Call a custom context function for this page, if it exists.
    if page.context:
        try:
            func = resolve_dotted_path(page.context)
        except (ImportError, AttributeError, ValueError), e:
            raise StandardError, 'The context function for this page does not exist. %s: %s' % (e.__class__.__name__, e)
        if args:
            response = func(request, context, args)
        else:
            response = func(request, context)
        if response:
            return response


    for n, position in enumerate(POSITIONS):
        position = position[0]

        if preview and position == preview.position:
            page_content = preview
        else:
            page_content = page.get_content(language, position=position)

        if n == 0:
            # This is the main page content.
            context.update({
                'page_content':page_content,
                'page_title': page_content.page_title or page_content.title,
            })

        title_dict[position], content_dict[position] = render_pagecontent(page_content, context)

    context.update({
        'content': content_dict,
        'title': title_dict,
    })

    # Third processing stage: Use the specified template
    # Templates are chosen in the following order:
    # 1. template defined in page (over `page_content.prepare()`)
    # 2. template defined in function arg "template_name"
    # 3. template defined in settings.DEFAULT_TEMPLATE
    # If preview, then _preview is appended to the templates name. If there's no preview template: fallback to the normal one
    if template_name:
        template_path = template_name
    elif page.template:
        template_path = page.template
    else:
        template_path = DEFAULT_TEMPLATE

    if preview: # append _preview to template name
        if template_path.endswith('.html'):
            template_path_preview = template_path[:template_path.rfind('.html')] + '_preview.html'
        else:
            template_path_preview += '_preview'
        try:
            template = loader.get_template(template_path_preview)
        except TemplateDoesNotExist:
            template = loader.get_template(template_path)
    else:
        try:
            template = loader.get_template(template_path)
        except TemplateDoesNotExist:
            if settings.DEBUG:
                raise
            else:
                template = loader.get_template(DEFAULT_TEMPLATE)

    return HttpResponse(template.render(context))


def handle_page(request, language, url):
    # TODO: Objects with overridden URLs have two URLs now. This shouldn't be the case.

    # First take a look if there's a navigation object with an overridden URL
    pages = Page.objects.filter(override_url=True, overridden_url=url, redirect_to__isnull=True)
    if pages:
        return render_page(request, language, pages[0])

    # If not, go and look it up
    parts = url and url.split('/') or []

    root = Page.objects.root()

    if not parts and not DISPLAY_ROOT:
        try:
            return HttpResponsePermanentRedirect(Page.objects.filter(parent=root)[0].get_absolute_url(language))
        except IndexError:
            raise RootPageDoesNotExist, unicode(_('Please create at least one subpage or enable DISPLAY_ROOT.'))

    parent = root
    pages = None
    args = []
    language_redirect_required = None
    for part in parts:
        pages = parent.page_set.filter(Q(slug=part) | Q(pagecontent__slug=part)) or parent.page_set.filter(slug='*')
        if not pages:
            raise Http404
        page = pages[0]
        pagecontent_in_language = page.pagecontent_set.filter(language=language)
        if pagecontent_in_language and pagecontent_in_language[0].slug and pagecontent_in_language[0].slug != part:
            language_redirect_required = True
        parent = page
        if parent.slug == '*':
            args.append(part)
            
    if not pages:
        page = root
    if page.redirect_to:
        return HttpResponsePermanentRedirect(page.redirect_to.get_absolute_url(language))
    if language_redirect_required:
        return HttpResponsePermanentRedirect(page.get_absolute_url(language))

    return render_page(request, language, page, args)


def handler(request):
    """
    Main handler view that calls the views to render a page or redirects to
    the appropriate language URL.
    """
    url = request.path
    urljunks = filter(lambda non_empty_junk: non_empty_junk, url.split('/'))
    languages = language_list()
    language = None

    # Skip multiple slashes in the URL
    if '//' in url:
        url = re.sub("/+" , "/", url)
        return HttpResponseRedirect('%s' % url)

    try:
        request_language = request.LANGUAGE_CODE[:2]
    except AttributeError:
        raise StandardError, "Please add django.middleware.locale.LocaleMiddleware to your MIDDLEWARE_CLASSES."

    # This shouldn't happen
    if not request_language in languages:
        request_language = settings.LANGUAGE_CODE[:2]
    if not request_language in languages:
        request_language = LANGUAGE_DEFAULT[:2]
    if not request_language in languages:
        try:
            request_language = languages[0]
        except:
            raise Exception, _("Please define LANGUAGES in your project's settings.")

    # Determine the language and redirect the user, if required
    if LANGUAGE_REDIRECT:
        if len(urljunks):
            url_language = urljunks[0]
            if url_language in languages:
                # Check request language against url language and change if necessary.
                # This allows django i18n language change over URL (and violates a lot of specs).
                # Requires a redirect to let django's locale middleware handle the statechange.
                if request_language != url_language:
                    request_language = url_language
                    if hasattr(request, 'session'):
                        request.session['django_language'] = url_language
                    else:
                        response = HttpResponseRedirect(url)
                        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, url_language)
                        return response
                    translation.activate(request_language)
                return handle_page(request, request_language, '/'.join(urljunks[1:]))
        if url == '/':
            # Don't redirect root
            return handle_page(request, request_language, '')
        return HttpResponsePermanentRedirect('/%s%s' % (request_language, url))
    return handle_page(request, request_language, url[1:-1])

if REQUIRE_LOGIN:
    handler = staff_member_required(handler)

def set_language(request):
    """
    Redirect to a given url while setting the chosen language in the
    session or cookie. The url and the language code need to be
    specified in the request parameters.

    Since this view changes how the user will see the rest of the site, it must
    only be accessed as a POST request. If called as a GET request, it will
    redirect to the page in the request (the 'next' parameter) without changing
    any state.
    """
    next = request.REQUEST.get('next', None)
    redirect = False
    if not next:
        next = request.META.get('HTTP_REFERER', None)
    if next:
        url_junks = next.split('/')
        if url_junks[0].startswith('http'):
            offset = 3
            next = '/'
        else:
            offset = 0
            next = ''
        if LANGUAGE_REDIRECT:
            if url_junks[offset] in language_list():
                redirect = True
                del url_junks[offset]
        next += '/'.join(url_junks[offset:])
    else:
        next = '/'
    response = HttpResponseRedirect('/')
    if request.method in ('POST', 'GET'):
        lang_code = request.REQUEST.get('language', None)
        if lang_code and check_for_language(lang_code):
            if LANGUAGE_REDIRECT and redirect:
                if lang_code in language_list():
                    next = u'/%s%s' % (lang_code, next)
            if hasattr(request, 'session'):
                request.session['django_language'] = lang_code
            else:
                response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
    response['Location'] = iri_to_uri(next)
    return response

def search(request, form_class=SearchForm, extra_context={}, 
        template_name="cms/search.html"):
    """
    Performs a search over Page and PageContent fields depending on the
    current language and also returns the search results for other languages.
    """

    language = request.LANGUAGE_CODE[:2]
    page = Page.objects.root()
    context = get_page_context(request, language, page)

    if request.GET.get('query', False):
        # create search form with GET variables if given
        search_form = form_class(request.GET)

        if search_form.is_valid():
            query = search_form.cleaned_data['query']

            # perform actual search
            search_results = Page.objects.search(request.user, query, language)
            page_ids = [res['id'] for res in search_results.values('id')]
            search_results_ml = Page.objects.search(request.user, query).exclude(id__in=page_ids)

            # update context to contain query and search results
            context.update({
                'search_results': search_results,
                'search_results_ml': search_results_ml,
                'query': query,
            })
    else:
        search_form = form_class()

    context.update({
        'search_form': search_form,
    })
    return render_to_response(template_name, extra_context,
        context_instance=RequestContext(request, context))

def get_tinymce_link_list(request):
    link_list = [(smart_unicode(page.get_path()), page.get_absolute_url()) for page in Page.objects.all()]
    output = "var %s = %s" % ("tinyMCELinkList", simplejson.dumps(link_list))
    return HttpResponse(output, content_type='application/x-javascript')
