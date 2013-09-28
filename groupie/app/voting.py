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
    from_email = voting.from_email
    url = "http://localhost:8000/{}".format(voting.url_hash)

    for vr in voting.voters.all():
        body = url + "?ref={}".format(vr.ref_hash)
        send_mail(subject, body, from_email, [vr.email])

    if voting.send_to_all:
        to_emails = [vr.email for vr in voting.voters.all()]
        body = "DISCUSS! {}".format(url)
        send_mail(subject, body, from_email, to_emails)

    # deadline reminders scheduling
    if voting.deadline:
        # TODO: schedule sending of deadline reminder; we need to remember to cancel it if voting changes
        pass
