from jinja2 import Environment
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from app1.models import CSVFile

import pandas as pd



def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })

    return env




# TEMPLATED DELIVERY
class HomeView(TemplateView):

    def get(self, request, *args, **kwargs):

        return render(request, 'app1/index.html', {})






# FUNCTIONAL DELIVERY
def get_data(request):

    df = pd.read_csv(CSVFile.objects.all()[0].csvFile)

    x = df.orgSize.to_list()
    y = df.Cadence.to_list()
    # z = df.Participant.to_list()

    data = {
        'coords': [
            {'x': a,
             'y': b,
                # 'z': c,
            }
                for (a, b) in zip(x, y)
        ]

    }

    return JsonResponse(data)







# DJANGO REST DELIVERY
class ChartData(APIView):
    authentication_classes = []
    permission_classes = []


    def get(self, request, format=None):

        df = pd.read_csv(CSVFile.objects.all()[0].csvFile)

        x = df.Participant.to_list()
        y = df.orgSize.to_list()
        z = df.Cadence.to_list()

        data = {
            'coords': [
                {'x': a,
                 'y': b,
                    # 'z': c,
                }
                    for (a, b) in zip(x, y)
            ],
            'labels': [str(s) for s in z],
        }
        return Response(data)
