import csv
import json
import requests
from datetime import datetime
from django import forms
from django.conf import settings
from django.http import HttpResponse
from django.core.cache import cache
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


def home(request):
    return render(request, 'home.html')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


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


KIBOT_HISTORY_URL_BASE = 'http://api.kibot.com/?action=history&splitadjusted=1'

def kibot_fetch_history(symbol, interval, period):
    url = KIBOT_HISTORY_URL_BASE + '&symbol={}&interval={}&period={}'.format(
        symbol, interval, period
    )

    resp = requests.get(url)
    if resp.text == '401 Not Logged In':
        requests.get('http://api.kibot.com/?action=login&user=guest&password=guest')
        resp = requests.get(url)

    if resp.status_code != 200:
        raise Exception('Error calling kibot. Got status code: ' + resp.status_code)

    fieldnames = ['dt', 'o', 'h', 'l', 'c', 'vol']
    reader = csv.DictReader(resp.text.split('\n'), fieldnames=fieldnames)
    return list(reader)


def feed(request):
    symbol = request.GET['symbol']
    interval = request.GET['interval']
    period = request.GET['period']

    cache_key = 'kibot-history-{}-{}-{}'.format(symbol, interval, period)
    cached = cache.get(cache_key)
    if cached:
        values = json.loads(cached)
    else:
        values = kibot_fetch_history(symbol, interval, period)
        cache.set(cache_key, json.dumps(values), 300)

    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['dt', 'o', 'h', 'l', 'c', 'vol'])

    for value in values:
        writer.writerow([
            datetime.strptime(value['dt'], '%m/%d/%Y').strftime('%Y-%m-%d %H:%M:%S'),
            value['o'],
            value['h'],
            value['l'],
            value['c'],
            value['vol'],
        ])

    return response
