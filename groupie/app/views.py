# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.http import HttpResponseRedirect
from django.shortcuts import render

from groupie.app.forms import VotingForm
from groupie.app.models import Voting
from groupie.app.voting import setup_voting


SAMPLE_DATA = {
    'from_email': "foobar@foo.bar",
    'description': "foo bar bar foo?",
    'deadline': datetime.now() + timedelta(seconds=10),
    'send_to_all': True,
    'emails': "a@a.com, b@b.com, c@c.com",
    'voting_options': "hey apple # hey orange # hey kiwi"
}


def home(request):
    if request.method == 'POST':
        form = VotingForm(request.POST)
        if form.is_valid():
            voting = form.save()
            setup_voting(voting)
            return HttpResponseRedirect('/{}?ref={}'.format(voting.url_hash, voting.creator.ref_hash))
    else:
        form = VotingForm(initial=SAMPLE_DATA)
    return render(request, 'home.html', {'form': form})


def voting(request, vote_hash):
    # TODO: based on ref in GET prefill "voter" field when voting
    # or add admin options if creator
    v = Voting.objects.get(url_hash=vote_hash)
    return render(request, 'voting.html', {'voting': v})
