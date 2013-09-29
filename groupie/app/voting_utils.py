# -*- coding: utf-8 -*-
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from iron_worker import IronWorker

from groupie.app import utils

worker = IronWorker()


def setup_voting(voting):
    # creator automatically votes for all proposed options
    vote(voting.creator, voting.voting_options.all())

    notify_create(voting)

    if voting.deadline:
        worker.queue(start_at=voting.deadline, code_name="notify_deadline",
                     payload={'url': utils.get_abs_deadline_hack_url(voting)})


def vote(voter, voting_options):
    # clear previous votes and cast new ones
    voter.voted_voting_options.clear()
    for vo in voting_options:
        vo.voters.add(voter)

    voters_all = voter.voting.voters.all()
    voters_not_voted = voters_all.filter(voted_voting_options__isnull=True).count()

    # send notifications if progress thresholds reached for the first time
    if not voter.voting.notify_all_voted_at and voters_not_voted == 0:
        notify_all_voted(voter.voting)
        # TODO cancel deadline notification
    elif voters_all.count() > 3 and not voter.voting.notify_half_voted_at and (voters_all.count() / 2.0) >= voters_not_voted:
        notify_half_voted(voter.voting)


## NOTIFICATIONS ##

def notify_create(voting):
    notify(voting, voting.voters.all(), "[groupie-hello-kitty]", "emails/created.html")
    voting.notify_created_at = timezone.now()
    voting.save()


def notify_deadline(voting):
    notify(voting, voting.voters.all(), "[groupie-no-jokes]", "emails/deadline.html")
    voting.notify_created_at = timezone.now()
    voting.save()


def notify_half_voted(voting):
    voters = voting.voters.filter(voted_voting_options__isnull=True)
    notify(voting, voters, "[groupie-getting-there...]", 'emails/half_voted.html')
    voting.notify_half_voted_at = timezone.now()
    voting.save()


def notify_all_voted(voting):
    notify(voting, voting.voters.all(), "[groupie-its-decided!]", 'emails/all_voted.html')
    voting.notify_all_voted_at = timezone.now()
    voting.save()


def notify(voting, voters, subject_tag, template):
    subject = "{} {}".format(subject_tag, voting.description_short)

    for vr in voters:
        body = render_to_string(template, {
            'voting': voting,
            'voting_url': utils.get_abs_url(voting, vr.ref_hash)
        })
        send_mail(subject, body, voting.from_email, [vr.email])
