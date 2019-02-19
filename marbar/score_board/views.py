from django.urls import reverse
from django.shortcuts import render, redirect, HttpResponse
from .models import ScoreUnit
from management.models import MarBar
from django.http import JsonResponse
import json
from django.contrib import messages


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
    try:
        active_marbar = MarBar.objects.get(is_active=True)
        all_data = ScoreUnit.objects.filter(marbar__pk=active_marbar.pk).order_by('title')
        return render(request, 'score_board.html',
                            {'collum_0': help_order(all_data.filter(placement=0)),
                             'collum_1': help_order(all_data.filter(placement=1)),
                             'collum_2': help_order(all_data.filter(placement=2)),
                             'collum_3': help_order(all_data.filter(placement=3)),
                             'collum_4': help_order(all_data.filter(placement=4)),
                             'countdown_date': active_marbar.end_date})
    except:
        return render(request, 'score_board.html', {})


def get_points(request):
    active_marbar = MarBar.objects.get(is_active=True)
    all_data = ScoreUnit.objects.filter(marbar__pk=active_marbar.pk).order_by('title')
    return JsonResponse(help_order_v2(all_data), safe=False)


def get_graph(request):
    active_marbar = MarBar.objects.get(is_active=True)
    D = ScoreUnit.objects.filter(marbar__pk=active_marbar.pk).order_by('title')
    points = []
    labels = []
    for d in D:
        points.append(d.points)
        labels.append(d.title)
    fin = [a for a in zip(labels, points)]
    #return JsonResponse({'points': json.dumps(points), 'graph_labels': json.dumps(labels)}, safe=False)
    return JsonResponse({'points': json.dumps(fin)}, safe=False)


def assign_points(request):
    active_bar = MarBar.objects.filter(is_active=True)
    if active_bar.exists():
        active_bar = MarBar.objects.get(is_active=True)
        if request.user.is_authenticated and (request.user in active_bar.users.all() or request.user.is_superuser):
            if request.method == 'GET':
                all_data = ScoreUnit.objects.filter(marbar__pk=active_bar.pk).order_by('title')
                return render(request, 'assign_points.html',
                                      {'collum_0': all_data.filter(placement=0),
                                       'collum_1': all_data.filter(placement=1),
                                       'collum_2': all_data.filter(placement=2),
                                       'collum_3': all_data.filter(placement=3),
                                       'collum_4': all_data.filter(placement=4)})
            elif request.method == 'POST':
                try:
                    su = ScoreUnit.objects.get(pk=int(request.POST.get('scoreUnitPk')))
                    new_val = request.POST.get('scoreUnitValue')
                    if new_val:
                        if new_val[0] == '-':
                            front_opr = -1
                            new_val = new_val[1:]
                        elif new_val[0] == '+':
                            front_opr = 1
                            new_val = new_val[1:]
                        else:
                            front_opr = 1
                        if str.isdigit(new_val):
                            new_score = su.points + (front_opr * int(new_val))
                            if new_score < 0:
                                new_score = 0
                            su.points = new_score
                            su.save()
                        else:
                            messages.add_message(request, messages.ERROR,
                                                 'The points field was not correctly filled and the points was not added')
                            return redirect(reverse('score_board:assign_points'))
                    else:
                        messages.add_message(request, messages.ERROR,
                                             'The points field was not correctly filled and the points was not added')
                        return redirect(reverse('score_board:assign_points'))

                    return redirect(reverse('score_board:assign_points'))
                except:
                    messages.add_message(request, messages.ERROR, 'An error occurred and the points was not added')
                    return redirect(reverse('score_board:assign_points'))
            else:
                return redirect(reverse('score_board'))
        else:
            messages.add_message(request, messages.ERROR,
                                 'You must be logged in and connected to the Active MarBar to access this')
            return redirect(reverse('score_board'))
    else:
        messages.add_message(request, messages.ERROR, 'There is no active MarBar at this time')
        return redirect(reverse('score_board'))
