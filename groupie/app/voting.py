# -*- coding: utf-8 -*-
from django.core.mail import send_mail

from groupie.app.models import Voter


def setup_voting(voting):
    # voting creator is added and automatically votes for all proposed options
    v = Voter.objects.create(email=voting.from_email, voting=voting)
    for vo in voting.voting_options.all():
        vo.voters.add(v)

    # notification emails sendings
    subject = "new groupie"
    body = "http://localhost:8000/{}".format(voting.url_hash)
    from_email = voting.from_email

    if voting.send_to_all:
        to_emails = [vr.email for vr in voting.voters.all()]
        send_mail(subject, body, from_email, to_emails)

        # creator gets an additional email with referer to give admin rights on voting page
        vr = voting.creator
        body += "?ref={}".format(vr.ref_hash)
        send_mail(subject, body, from_email, [vr.email])

    else:
        # each user gets a separate email with a referer to identify him while voting
        for vr in voting.voters:
            body += "?ref={}".format(vr.ref_hash)
            send_mail(subject, body, from_email, [vr.email])

    # deadline reminders scheduling
    if voting.deadline:
        # TODO: schedule sending of deadline reminder; we need to remember to cancel it if voting changes
        pass
