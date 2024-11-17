from django.template import loader
from django.http import Http404, HttpResponse
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

def render_error_page(request,context, exception=None):
    if exception:
        logger.error(str(exception))
        #  check exception is of type Http404
        if isinstance(exception, Http404):
            return render_404_page(context, request, exception)
        else:
            return render_500_page(request,context, exception)
    else:
        return render_404_page(context, request, exception)
def render_500_page(request,context, exception=None):
    if exception:
        logger.error(str(exception))
    html_template = loader.get_template('home/page-500.html')
    return HttpResponse(html_template.render(context, request))

def render_404_page(context, request, exception=None):
    if exception:
        logger.error(str(exception))
    html_template = loader.get_template('home/page-404.html')
    return HttpResponse(html_template.render(context, request))