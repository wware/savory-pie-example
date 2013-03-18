import json

from django.contrib.auth.decorators import login_required
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response

from models import Zone, Content, ZoneContent


# @login_required(login_url='/login/')

def home(request):

    lst = [z.to_json() for z in Zone.objects.all()]
    #import pdb; pdb.set_trace()
    return render_to_response('base.html', {
        'zones': [z.to_json() for z in Zone.objects.all()],
        'contents': [z.to_json() for z in Content.objects.all()],
        'zonecontents': [z.to_json() for z in ZoneContent.objects.all()],
        })

