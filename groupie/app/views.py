# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render


from groupie.app.forms import VotingForm


SAMPLE_DATA = {
    'from_email': "foobar@foo.bar",
    'description': "foo bar bar foo?",
    'deadline': datetime.now() + timedelta(seconds=10),
    'send_to_all': True,
    'emails': "a@a.com, b@b.com, c@c.com",
    'options': "hey apple # hey orange # hey kiwi"
}


def home(request):
    ## process 'GET'
    if request.method == 'GET':
        form = VotingForm(initial=SAMPLE_DATA)
        return render(request, 'home.html', {'form': form})

    ## process 'POST'
    form = VotingForm(request.POST)

    if not form.is_valid():
        # form invalid - show errors
        return render(request, 'home.html', {'form': form})

    voting, voting_options, voters = form.save()
    # form valid - show voting page
    return HttpResponseRedirect('/{}'.format(voting.url_hash))


def voting(request, vote_hash):
    return HttpResponse("TODO: FIXME ;)")
