# -*- coding: utf-8 -*-
from django.core.mail import send_mail
from django.template.loader import render_to_string

from groupie.app import utils


def setup_voting(voting):
    # creator automatically votes for all proposed options
    vote(voting.creator, voting.voting_options.all())

    # send creation notifications
    notify_all(voting, voting.voters.all(), "[groupie-hello-kitty]", "create")

    # deadline reminders scheduling
    if voting.deadline:
        # TODO: schedule sending of deadline reminder; we need to remember to cancel it if voting changes
        pass


def vote(voter, voting_options):
    voter.voted_voting_options.clear()
    for vo in voting_options:
        vo.voters.add(voter)

    # TODO: make those notifications be sent only once
    # send notifications if progress thresholds reached
    voters_all = voter.voting.voters.all()
    voters_not_voted = voter.voting.voters.filter(voted_voting_options__isnull=True)
    if voters_not_voted.count() == 0:
        # TODO: show only top voted
        notify_all(voter.voting, voter.voting.voters.all(), "[groupie-its-decided!]", 'all_voted')
    elif (voters_all.count() / 2.0) >= voters_not_voted.count():
        notify_all(voter.voting, voters_not_voted, "[groupie-getting-there...]", 'half_voted')


def notify_all(voting, voters, subject_tag, template_name):
    subject = "{} {}".format(subject_tag, voting.description_short)
    from_email = voting.from_email

    for vr in voters:
        body = render_to_string("emails/{}.html".format(template_name), {
            'voting': voting,
            'voting_url': utils.get_abs_url(voting, vr.ref_hash)
        })
        send_mail(subject, body, from_email, [vr.email])
