# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from groupie.app import utils
from groupie.app.forms import VotingAddForm
from groupie.app.models import Voting, Voter, VotingOption
from groupie.app.voting import setup_voting, vote


@require_http_methods(["GET", "POST"])
def home(request):
    if request.method == 'POST':
        form = VotingAddForm(request.POST)
        if form.is_valid():
            voting = form.save()
            setup_voting(voting)
            redirect_url = utils.get_abs_url(voting, voting.creator.ref_hash)
            return HttpResponseRedirect(redirect_url)

        context = {'form': form}
    else:
        context = {}

    return render(request, 'home.html', context)


@require_http_methods(["GET", "POST"])
def voting(request, voting_hash):
    # referer is mandatory
    ref = request.GET['ref']
    voter = Voter.objects.get(ref_hash=ref)

    v = Voting.objects.get(url_hash=voting_hash)
    if request.method == 'POST':
        vos_ids = [int(vo) for vo in request.POST.getlist('voting_options') if vo]
        vos = VotingOption.objects.filter(id__in=vos_ids, voting=v)
        vote(voter, vos)

    vos = sorted(v.voting_options.all(), key=lambda vo: vo.voters.count(), reverse=True)
    voting_options_sorted = [{'option': vo, 'is_top': vo.voters.count() == vos[0].voters.count()} for vo in vos]

    ctx = {
        'voting': v,
        'voter': voter,
        'is_creator': voter == v.creator,
        'voting_options_sorted': voting_options_sorted
    }
    return render(request, 'voting.html', ctx)
