
from django.shortcuts import render_to_response

from theming.models import thememanager


def index(request):
    print 'rendering with', thememanager.get_current_theme()
    return render_to_response('simpleapp_index.html')

