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
import re, random



###### READ IN CSVs ##############
df = (tmp := pd.read_csv(CSVFile.objects.all()[0].csvFile.name,
                        usecols=['Text',
                                'Tag',
                                'Tag - Group',
                                'Note - Role',
                                'Note - Industry',
                                'Note - Participant ID'])
     ).drop(
    tmp.loc[tmp['Note - Participant ID'].str.contains('MKT'), :].index).rename(
    {'Text': 'Evidence',
     'Tag - Group': 'Group',
     'Note - Role': 'Role',
     'Note - Industry': 'Industry',
     'Note - Participant ID': 'Participant'}, axis=1).dropna()

orgdf = (tmp := pd.read_csv(CSVFile.objects.all()[1].csvFile.name)).drop(tmp.loc[tmp['Participant ID'].str.contains('P4'), :].index)

parDict = {int(x.split('P')[-1]): f"P{int(x.split('P')[-1])}" for x in df.Participant.unique()}

df['Participant'] = df['Participant'].map(lambda x: {v: k for k, v in parDict.items()}[f"P{int(x.split('P')[-1])}"])
orgdf['Participant ID'] = orgdf['Participant ID'].map(lambda x: {v: k for k, v in parDict.items()}[f"P{int(x.split('P')[-1])}"])

df['orgSize'] = df['Participant'].map(lambda x: orgdf[orgdf['Participant ID'] == x]['Org Size'].item()
                                      .replace(' to ', '-').replace(' +', '-99,999').replace('1000-4999', '1,000-4,999'))

orgDict = {int(re.split(r'\D', x.replace(',', ''))[0]): x for x in df.orgSize}
del df, orgdf
####################################


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

        file_name = CSVFile.objects.all()[2].csvFile.name

        df = pd.read_csv('{}'.format(file_name))


        return render(request, 'app1/index.html', {'data': {
            'columns': {
                x: df[x].to_list() for x in df.columns
            },
            'parDict': parDict,
            'orgDict': orgDict
        }})






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

        df = pd.read_csv(CSVFile.objects.all()[2].csvFile).astype('category')

        xValues = [p + random.uniform(-0.05, 0.05) for p in df.orgSize.cat.codes.to_list()]
        yValues = [i + random.uniform(-0.05, 0.05) for i in df.Cadence.cat.codes.to_list()]
        labels = df.Participant.to_list()

        data = {
            'coords': [
                {'x': x,
                 'y': y
                } for x, y in zip(xValues, yValues)
            ],
            'labels': labels
        }

        return Response(data)