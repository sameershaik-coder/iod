from django.template import loader
from django.http import HttpResponse

def demo(request):
    context = {'segment': 'demo'}

    #html_template = loader.get_template('esite/home/others/pages-landingpage.html')
    html_template = loader.get_template('extsite/home/index.html')
    return HttpResponse(html_template.render(context, request))