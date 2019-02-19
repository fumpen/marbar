from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import MarBar, Event
from .forms import MarBarForm, EventForm
from score_board.models import ScoreUnit
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction


def general_management(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO, 'plz log in to access this site')
        return redirect(reverse('management:login_view'))
    else:
        response_context = {}
        if request.user.is_superuser:
            response_context['superuser'] = True
            response_context['createUser'] = UserCreationForm

            marbar_form = MarBarForm()
            response_context['createMarBar'] = marbar_form
            marbars = MarBar.objects.all()
        else:
            response_context['superuser'] = False
            marbars = MarBar.objects.filter(users__in=[request.user])

        t = [{'title': m.title, 'pk': m.pk,
              'form': MarBarForm({'title': m.title, 'users': m.users, 'end_date': m.end_date, 'intended_pk': m.pk})}
             for m in marbars]

        response_context['manageMarbars'] = t
        return render(request, 'manage_marbar.html', response_context)



def crude_login_view(request):
    return render(request, "login.html")


def crude_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(reverse('management:management_view'))
    else:
        messages.add_message(request, messages.ERROR, 'Either username or password were incorrect')
        return redirect(reverse('management:login_view'))


def logout_user(request):
    logout(request)
    return redirect(reverse('score_board'))


def create_marbar(request):
    if not request.user.is_authenticated & request.user.is_superuser:
        messages.add_message(request, messages.INFO, 'plz log in to access this site')
        return redirect(reverse('management:login_view'))
    if request.method == 'POST':
        form = MarBarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(new_instance=True)
            messages.add_message(request, messages.INFO, 'MarBar was successfully created')
            return redirect(reverse('management:management_view'))
        else:
            messages.add_message(request, messages.WARNING, "Please recheck that the form is filled as intended")
            return redirect(reverse('management:management_view'))
    else:
        messages.add_message(request, messages.ERROR,
                             "You have beers to drink and records to break, Stop playing around")
        return redirect(reverse('management:management_view'))


def create_user(request):
    if not request.user.is_authenticated & request.user.is_superuser:
        messages.add_message(request, messages.INFO, 'plz log in to access this site')
        return redirect(reverse('management:login_view'))
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'User was successfully created')
            return redirect(reverse('management:management_view'))
        else:
            messages.add_message(request, messages.WARNING, "The user input did not fulfill with the requirements")
            return redirect(reverse('management:management_view'))
    else:
        messages.add_message(request, messages.ERROR,
                             "You have beers to drink and records to break, Stop playing around")
        return redirect(reverse('management:management_view'))


def update_marbar(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO, 'plz log in to access this site')
        return redirect(reverse('management:login_view'))
    if request.method == 'POST':
        form = MarBarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(new_instance=False, update_instance=True)
            messages.add_message(request, messages.INFO, 'MarBar was successfully updated')
            return redirect(reverse('management:management_view'))
        else:
            messages.add_message(request, messages.WARNING, "Please recheck that the form is filled as intended")
            return redirect(reverse('management:management_view'))
    else:
        messages.add_message(request, messages.ERROR,
                             "You have beers to drink and records to break, Stop playing around")
        return redirect(reverse('management:management_view'))


def activate_marbar(request):
    if not request.user.is_authenticated & request.user.is_superuser:
        messages.add_message(request, messages.INFO, 'plz log in to access this site')
        return redirect(reverse('management:login_view'))
    if request.method == 'POST':
        if 'activateMarBar' in request.POST:
            activation_pk = int(request.POST.get('activateMarBar'))
            try:
                m = MarBar.objects.get(pk=activation_pk)
                if not m.is_active:
                    with transaction.atomic():
                        if MarBar.objects.filter(is_active=True).exists():
                            old_active = MarBar.objects.get(is_active=True)
                            old_active.is_active = False
                            old_active.save()
                        m.is_active = True
                        m.save()
                        messages.add_message(request, messages.INFO, '{} is now the active MarBar'.format(m.title))
                else:
                    messages.add_message(request, messages.INFO, 'This MarBar is already active')
            except ObjectDoesNotExist:
                messages.add_message(request, messages.WARNING, 'An error occurred, please try again')
            return redirect(reverse('management:management_view'))
        else:
            messages.add_message(request, messages.WARNING, "Refresh the page or contact someone that has coded this")
            return redirect(reverse('management:management_view'))
    else:
        messages.add_message(request, messages.ERROR,
                             "You have beers to drink and records to break, Stop playing around")
        return redirect(reverse('management:management_view'))


def events_view(request):
    active_bar = MarBar.objects.filter(is_active=True)
    if active_bar.exists() and active_bar.count() == 1:
        active_bar = MarBar.objects.get(is_active=True)
        if request.method == 'GET':
            response_context = {}
            events = Event.objects.filter(marbar=active_bar).order_by('start_date')
            if events.exists():
                response_context = {'current_events': [e for e in events]}

            if request.user.is_authenticated and (request.user in active_bar.users.all() or request.user.is_superuser):
                response_context['event_form'] = EventForm()
            return render(request, 'events.html', response_context)

        elif request.method == 'POST':
            if request.user.is_authenticated and (request.user in active_bar.users.all() or request.user.is_superuser):
                new_event = EventForm(request.POST)
                if new_event.is_valid():
                    new_event.save(active_marbar=active_bar)
                    messages.add_message(request, messages.INFO, 'Event was successfully created')
                    return redirect(reverse('management:events'))
                else:
                    messages.add_message(request, messages.WARNING, 'Please recheck the information filled in the from')
                    return redirect(reverse('management:events'))
            else:
                messages.add_message(request, messages.WARNING, 'Please log in again to access this functionality')
                return redirect(reverse('management:login'))

        else:
            return redirect(reverse('score_board'))
    else:
        messages.add_message(request, messages.ERROR, 'There is currently no active MarBar')
        return redirect(reverse('score_board'))


def delete_event(request):
    active_bar = MarBar.objects.filter(is_active=True)

    if active_bar.exists() and active_bar.count() == 1:
        active_bar = MarBar.objects.get(is_active=True)
        if request.user.is_authenticated and (request.user in active_bar.users.all() or request.user.is_superuser):
            if request.method == 'POST':
                try:
                    e = Event.objects.get(pk=int(request.POST.get('event_pk')), marbar=active_bar)
                    e.delete()
                    messages.add_message(request, messages.INFO, 'The event was deleted')
                    return redirect(reverse('management:events'))
                except:
                    messages.add_message(request, messages.ERROR, 'Refresh the page and try again')
                    return redirect(reverse('management:events'))
            else:
                messages.add_message(request, messages.ERROR, 'Stop fooling around!')
                return redirect(reverse('management:events'))
        else:
            messages.add_message(request, messages.INFO, 'plz log in to access this functionality')
            return redirect(reverse('management:login_view'))
    messages.add_message(request, messages.ERROR, 'There is currently no active MarBar')
    return redirect(reverse('score_board'))

