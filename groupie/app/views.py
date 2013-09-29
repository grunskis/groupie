# -*- coding: utf-8 -*-
from functools import wraps

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from groupie.app.forms import VotingAddForm
from groupie.app.models import Voting, Voter, VotingOption
from groupie.app.voting import setup_voting


## HELPERS

def voter_from_referer(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        # referer is mandatory
        ref = request.GET['ref']
        setattr(request, 'voter', Voter.objects.get(ref_hash=ref))
        return function(request, *args, **kwargs)

    return decorator


## VIEWS

@require_http_methods(["GET", "POST"])
def home(request):
    if request.method == 'POST':
        form = VotingAddForm(request.POST)
        if form.is_valid():
            voting = form.save()
            setup_voting(voting)
            # TODO: use reverse
            return HttpResponseRedirect('/{}?ref={}'.format(voting.url_hash, voting.creator.ref_hash))

        context = {'form': form}
    else:
        context = {}

    return render(request, 'home.html', context)


@require_http_methods(["GET", "POST"])
@voter_from_referer
def voting(request, voting_hash):
    v = Voting.objects.get(url_hash=voting_hash)
    if request.method == 'POST':
        vos_ids = [int(vo) for vo in request.POST.getlist('voting_options') if vo]
        request.voter.voted_voting_options.clear()
        vos = VotingOption.objects.filter(id__in=vos_ids, voting=v)
        for vo in vos:
            vo.voters.add(request.voter)

    vos = sorted(v.voting_options.all(), key=lambda vo: vo.voters.count(), reverse=True)
    voting_options_sorted = [{'option': vo, 'is_top': vo.voters.count() == vos[0].voters.count()} for vo in vos]

    ctx = {
        'voting': v,
        'voter': request.voter,
        'is_creator': request.voter == v.creator,
        'voting_options_sorted': voting_options_sorted
    }
    return render(request, 'voting.html', ctx)


# from django.utils import simplejson
# from jsonview.decorators import json_view
#
#
# @json_view
# @voter_from_referer
# def option_add(request, voting_hash):
#     try:
#         v = Voting.objects.get(url_hash=voting_hash)
#     except Voting.DoesNotExist:
#         return {'status': 'error', 'error': 'Voting does not exist'}
#
#     data = simplejson.loads(request.raw_post_data)
#     try:
#         vo_text = data['voting_option']
#     except KeyError:
#         return {'status': 'fail', 'error': '"voting_option" missing in request JSON'}
#
#     if not vo_text:
#         return {'status': 'fail', 'error': '"voting_option" empty in request JSON'}
#
#     vo = VotingOption.objects.create(text=vo_text)
#     v.voting_options.add(vo)
#
#     return {'status': 'ok'}
