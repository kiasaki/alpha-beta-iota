import csv
import pytz
from datetime import datetime
from django import forms
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from app.utils import cached
from app.kibot import kibot_fetch_history
from app.forms import SignUpForm, AccountForm
from app.models import AssetType, AssetTickSummary


def home(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def trade(request):
    return render(request, 'trade.html')

@login_required
def research(request):
    return render(request, 'research.html')

@login_required
def games(request):
    return render(request, 'games.html')

@login_required
def accounts(request):
    return render(request, 'accounts.html')

@login_required
def accounts_new(request):
    if request.method == 'POST':
        account = Account(owner=request.user)
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('accounts')
    else:
        form = AccountForm()
    return render(request, 'accounts_new.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


new_york_tz = pytz.timezone('America/New_York')

def fetch_history(symbol, interval, period):
    values = kibot_fetch_history(symbol, interval, period)
    for value in values:
        dt = datetime.strptime(value['dt'] + ' 15:59:59', '%m/%d/%Y %H:%M:%S')
        value['dt'] = dt.strftime('%Y-%m-%d %H:%M:%S')
        value['o'] = int(float(value['o'])*10000)
        value['h'] = int(float(value['h'])*10000)
        value['l'] = int(float(value['l'])*10000)
        value['c'] = int(float(value['c'])*10000)
    return values


def feed(request):
    symbol = request.GET['symbol']
    interval = request.GET['interval']
    period = request.GET['period']

    if interval not in ('minute', 'daily', 'weekly', 'monthly'):
        return HttpResponse('Invalid interval provided', status=400)

    try:
        period = int(period)
    except ValueError:
        return HttpResponse('Invalid period provided', status=400)

    cache_key = 'kibot-history-{}-{}-{}'.format(symbol, interval, period)
    values, miss = cached(
        cache_key, 300,
        lambda: fetch_history(symbol, interval, period)
    )

    if miss:
        for value in values:
            AssetTickSummary.objects.get_or_create(
                dt=new_york_tz.localize(datetime.strptime(value['dt'], '%Y-%m-%d %H:%M:%S')),
                type=AssetType.STOCKS,
                sym=symbol,
                defaults={
                    'o': value['o'],
                    'h': value['h'],
                    'l': value['l'],
                    'c': value['c'],
                    'vol': value['vol'],
                }
            )

    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['dt', 'o', 'h', 'l', 'c', 'vol'])

    for value in values:
        writer.writerow([
            value['dt'],
            value['o']/10000,
            value['h']/10000,
            value['l']/10000,
            value['c']/10000,
            value['vol'],
        ])

    return response
