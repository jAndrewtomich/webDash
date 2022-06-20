from jinja2 import Environment
# from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework import authentication, permissions

from app2.models import CSVFile, Tag, Participant, Evidence
# from django.core.files import File

import pandas as pd
import re, random


###### READ IN CSVs ##############
# if not Participant.objects.all():
#     ogdf = (tmp := pd.read_csv(CSVFile.objects.get(name='new').csvFile.name,
#                             usecols=['Text',
#                                     'Tag',
#                                     'Tag - Group',
#                                     'Note - Role',
#                                     'Note - Industry',
#                                     'Note - Participant ID'])
#         ).drop(
#         tmp.loc[tmp['Note - Participant ID'].str.contains('MKT'), :].index).rename(
#         {'Text': 'Evidence',
#         'Tag - Group': 'Group',
#         'Note - Role': 'Role',
#         'Note - Industry': 'Industry',
#         'Note - Participant ID': 'Participant'}, axis=1).dropna()

#     orgdf = (tmp := pd.read_csv(CSVFile.objects.get(name='orgSize').csvFile.name)).drop(tmp.loc[tmp['Participant ID'].str.contains('P4'), :].index)

#     parDict = {int(x.split('P')[-1]): f"P{int(x.split('P')[-1])}" for x in ogdf.Participant.unique()}

#     ogdf['Participant'] = ogdf['Participant'].map(lambda x: {v: k for k, v in parDict.items()}[f"P{int(x.split('P')[-1])}"])
#     orgdf['Participant ID'] = orgdf['Participant ID'].map(lambda x: {v: k for k, v in parDict.items()}[f"P{int(x.split('P')[-1])}"])

#     ogdf['orgSize'] = ogdf['Participant'].map(lambda x: orgdf[orgdf['Participant ID'] == x]['Org Size'].item()
#                                         .replace(' to ', '-').replace(' +', '-99,999').replace('1000-4999', '1,000-4,999'))

#     orgDict = {int(re.split(r'\D', x.replace(',', ''))[0]): x for x in ogdf.orgSize}

#     ogdf.orgSize = ogdf.orgSize.map(lambda x: {v: k for k, v in orgDict.items()}[x])


#     for tup in ogdf.loc[:, 'Tag':'Group'].drop_duplicates().sort_values('Tag', ascending=False).reset_index().drop('index', axis=1).itertuples():
#         if tup[1] not in [t.name for t in Tag.objects.all()]:
#             t = Tag.objects.create(name=tup[1], group=tup[2])
#             t.save()

#     for tup in ogdf.loc[:, 'Role':'orgSize'].drop_duplicates().sort_values('Participant', ascending=False).reset_index().drop('index', axis=1).itertuples():
#         if f"RHI {str(tup[3])}" not in [p.name for p in Participant.objects.all()]:
#             p = Participant.objects.create(name=f"RHI {str(tup[3])}", role=tup[1], industry=tup[2], orgSize=tup[4])
#             p.save()

#             for e in ogdf.loc[ogdf.Participant == tup[3], 'Evidence'].unique():
#                 tags_list = ogdf.sort_values('Group', ascending=False).loc[ogdf.Evidence == e, 'Tag'].to_list()
#                 ev = Evidence.objects.create(text=f"{e[:197]}...", participant=Participant.objects.filter(name=f"RHI {str(tup[3])}")[0])
#                 ev.save()
#                 for t in tags_list:
#                     ev.tags.add(Tag.objects.filter(name=t)[0])
#                     ev.save()

#     del ogdf, orgdf
####################################


# def environment(**options):
#     env = Environment(**options)
#     env.globals.update({
#         'static': staticfiles_storage.url,
#         'url': reverse,
#     })

#     return env




# TEMPLATED DELIVERY
class HomeView(TemplateView):

    def get(self, request, *args, **kwargs):

        # file_name = CSVFile.objects.get(name='out2').csvFile.name

        # df = pd.read_csv('{}'.format(file_name))

        df = pd.read_csv('/home/at/coding/py/projects/rhi/jptr/output/out2.csv')

        # ogdf = (tmp := pd.read_csv(CSVFile.objects.get(name='new').csvFile.name,
        #                         usecols=['Text',
        #                                 'Tag',
        #                                 'Tag - Group',
        #                                 'Note - Role',
        #                                 'Note - Industry',
        #                                 'Note - Participant ID'])
        #     ).drop(
        #     tmp.loc[tmp['Note - Participant ID'].str.contains('MKT'), :].index).rename(
        #     {'Text': 'Evidence',
        #     'Tag - Group': 'Group',
        #     'Note - Role': 'Role',
        #     'Note - Industry': 'Industry',
        #     'Note - Participant ID': 'Participant'}, axis=1).dropna()

        # orgdf = (tmp := pd.read_csv(CSVFile.objects.get(name='orgSize').csvFile.name)).drop(tmp.loc[tmp['Participant ID'].str.contains('P4'), :].index)

        # parDict = {int(x.split('P')[-1]): f"P{int(x.split('P')[-1])}" for x in ogdf.Participant.unique()}

        # ogdf['Participant'] = ogdf['Participant'].map(lambda x: {v: k for k, v in parDict.items()}[f"P{int(x.split('P')[-1])}"])
        # orgdf['Participant ID'] = orgdf['Participant ID'].map(lambda x: {v: k for k, v in parDict.items()}[f"P{int(x.split('P')[-1])}"])

        # ogdf['orgSize'] = ogdf['Participant'].map(lambda x: orgdf[orgdf['Participant ID'] == x]['Org Size'].item()
        #                                     .replace(' to ', '-').replace(' +', '-99,999').replace('1000-4999', '1,000-4,999'))

        # orgDict = {int(re.split(r'\D', x.replace(',', ''))[0]): x for x in ogdf.orgSize}

        # del ogdf, orgdf

        return render(request, 'app1/index.html', {'data': {
            'columns': {
                x: df[x].to_list() for x in df.columns
            },
            # 'parDict': parDict,
            # 'orgDict': orgDict
        }})






# FUNCTIONAL DELIVERY
def get_data(request):

    df = pd.read_csv(CSVFile.objects.get(name='out').csvFile)

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

        df = pd.read_csv(CSVFile.objects.get(name='out2').csvFile).astype('category')

        xValues1 = [p + random.uniform(-0.05, 0.05) for p in df.modOrgSize.cat.codes.to_list()]
        yValues1 = [i + random.uniform(-0.05, 0.05) for i in df.Participant.cat.codes.to_list()]

        xValues2 = [f for f in df.Freq.cat.codes.to_list()]
        yValues2 = [p for p in df.Participant.cat.codes.to_list()]


        labels = df.Cadence.cat.categories.to_list()

        data = {
            'coords1': [
                {'x': x,
                 'y': y
                } for x, y in zip(xValues1, yValues1)
            ],
            'coords2': [
                {'x': x,
                 'y': y,
                } for x, y in zip(xValues2, yValues2)
            ],
            'labels': labels
        }

        del df, xValues1, xValues2, yValues1, yValues2, labels
        return Response(data)