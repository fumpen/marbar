from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import MarBar
from .forms import MarBarForm
from score_board.models import ScoreUnit
from django.contrib import messages


def general_management(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO, 'plz log in to access this site')
        return redirect(reverse('management:login_view'))
    else:
        marbars = MarBar.objects.filter(user=request.user)
        t = [{'marbar': m, 'scoreunit': ScoreUnit.objects.filter(marbar=m)} for m in marbars]
        m = ''
        response_context = {'info': t,
                   'message': m}
        if request.user.is_superuser:
            response_context['superuser'] = True
            response_context['createUser'] = UserCreationForm

            marbar_form = MarBarForm(user_choices=User.objects.all())
            response_context['createMarBar'] = marbar_form
        else:
            response_context['superuser'] = False
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
    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO, 'plz log in to access this site')
        return redirect(reverse('management:login_view'))
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'MarBar was sucessfully created')
            return redirect(reverse('management:management_view'))
        else:
            messages.add_message(request, messages.WARNING, "The user input did not comply with the requirements")
            return redirect(reverse('management:management_view'))
    else:
        messages.add_message(request, messages.ERROR, "How did you even hit this case!? Don't do that")
        return redirect(reverse('management:management_view'))


def create_user(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO, 'plz log in to access this site')
        return redirect(reverse('management:login_view'))
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'User was successfully created')
            return redirect(reverse('management:management_view'))
        else:
            messages.add_message(request, messages.WARNING, "The user input did not comply with the requirements")
            return redirect(reverse('management:management_view'))
    else:
        messages.add_message(request, messages.ERROR, "How did you even hit this case!? Don't do that")
        return redirect(reverse('management:management_view'))

