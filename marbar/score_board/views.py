from django.shortcuts import render
from .models import ScoreUnit
from django.http import JsonResponse
import json


def help_order(d):
    xs = []
    for x in d:
        xs.append(x)
    return xs

def help_order_v2(d):
    xs = []
    for x in d:
        xs.append({'title': x.title, 'points': x.points})
    return xs


def score_board(request):
    a = ScoreUnit
    all_data = ScoreUnit.objects.all().order_by('title')
    return render(request, 'score_board.html',
                        {'collum_0': help_order(all_data.filter(placement=0)),
                         'collum_1': help_order(all_data.filter(placement=1)),
                         'collum_2': help_order(all_data.filter(placement=2)),
                         'collum_3': help_order(all_data.filter(placement=3)),
                         'collum_4': help_order(all_data.filter(placement=4))})


def get_points(request):
    all_data = ScoreUnit.objects.all().order_by('title')
    return JsonResponse(help_order_v2(all_data), safe=False)


def get_graph(request):
    D = ScoreUnit.objects.all().order_by('title')
    points = []
    labels = []
    for d in D:
        points.append(d.points)
        labels.append(d.title)
    JsonResponse({'points': json.dump(points), 'labels': json.dump(labels)}, safe=False)

