# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from groupie.app import utils, voting_utils
from groupie.app.forms import VotingAddForm, VotingForm
from groupie.app.models import Voting, Voter, VotingOption


@require_http_methods(["GET", "POST"])
def home(request):
    if request.method == 'POST':
        form = VotingAddForm(request.POST)
        if form.is_valid():
            voting = form.save()
            voting_utils.setup_voting(voting)
            redirect_url = utils.get_abs_url(voting, voting.creator.ref_hash)
            return HttpResponseRedirect(redirect_url)

        emails = ','.join(form.cleaned_data['emails'])
        voting_options = form.cleaned_data['voting_options']
        context = {'form': form, 'emails': emails,
                   'voting_options': voting_options}
    else:
        context = {'emails': ''}

    return render(request, 'home.html', context)


@require_http_methods(["GET", "POST"])
def voting(request, voting_hash):
    # referer is mandatory
    ref = request.GET['ref']
    voter = Voter.objects.get(ref_hash=ref)

    v = Voting.objects.get(url_hash=voting_hash)
    if request.method == 'POST':
        form = VotingForm(request.POST, voting=v)

        if form.is_valid():
            ids = form.cleaned_data['options']
            voter.voted_voting_options.clear()
            vos = VotingOption.objects.filter(id__in=ids, voting=v)
            voting_utils.vote(voter, vos)

            messages.success(request, 'Your vote has been submitted! '
                             'Hang tight while others do the same...')
    else:
        initial_votes = v.voting_options.filter(
            voters__ref_hash=voter.ref_hash).values_list('id', flat=True)

        form = VotingForm(voting=v, initial={
            'options': initial_votes
        })

    voting_options = []
    for vo in v.voting_options.order_by('option'):
        voter_emails = list(vo.voters.values_list('email', flat=True))
        if voter.email in voter_emails:
            voter_emails[voter_emails.index(voter.email)] = 'You'

        if vo.voters.filter(email=voter.email).exists():
            vote = 'yes'
        else:
            vote = 'no'

        voting_options.append({
            'id': vo.id,
            'datetime': vo.option,
            'voters': ','.join(voter_emails),
            'nr_of_votes': len(voter_emails),
            'vote': vote
        })

    ctx = {
        'voting': v,
        'voting_options': voting_options,
        'voter': voter,
        'is_creator': voter == v.creator,
        'form': form
    }
    return render(request, 'voting.html', ctx)


@require_http_methods(["GET"])
def deadline_hack(request, voting_hash):
    voting_utils.notify_deadline(Voting.objects.get(url_hash=voting_hash))
    return HttpResponse()
