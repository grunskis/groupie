# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.http import HttpResponseRedirect
from django.shortcuts import render

from groupie.app.forms import VotingForm
from groupie.app.models import Voter, Voting


SAMPLE_DATA = {
    'from_email': "foobar@foo.bar",
    'description': "foo bar bar foo?",
    'deadline': datetime.now() + timedelta(seconds=10),
    'send_to_all': True,
    'emails': "a@a.com, b@b.com, c@c.com",
    'voting_options': "hey apple # hey orange # hey kiwi"
}


def setup_voting(voting):
    # voting creator is added and automatically votes for all proposed options
    v = Voter.objects.create(email=voting.from_email, voting=voting)
    for vo in voting.voting_options.all():
        vo.voters.add(v)

    # TODO: send emails

    # TODO: schedule sending of deadline reminder


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
    # TODO: based on ref in GET grant voting permissions 
    # or voting/editing if creator (check voter.email=voting.from_email
    v = Voting.objects.get(url_hash=vote_hash)
    return render(request, 'voting.html', {'voting': v})
