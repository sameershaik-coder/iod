from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django import template
from django.urls import reverse

# Create your views here.


def demo(request):
    context = {'segment': 'demo'}

    html_template = loader.get_template('demo/home/index.html')
    return HttpResponse(html_template.render(context, request))

def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[3]
        # if load_template == 'admin':
        #     return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        if ".html" in load_template:
            html_template = loader.get_template('demo/home/' + load_template)
        else:
            html_template = loader.get_template('demo/home/' + load_template+'.html')
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))