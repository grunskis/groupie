# -*- coding: utf-8 -*-
from django.core.mail import send_mail
from django.template.loader import render_to_string

from groupie.app import utils


def setup_voting(voting):
    # creator automatically votes for all proposed options
    for vo in voting.voting_options.all():
        vo.voters.add(voting.creator)

    # notification emails sendings
    subject = "[groupie] {}".format(voting.description_short)
    from_email = voting.from_email

    for vr in voting.voters.all():
        body = render_to_string('emails/create.html', {
            'voting': voting,
            'voting_url': utils.get_abs_url(voting, vr.ref_hash)
        })

        send_mail(subject, body, from_email, [vr.email])

    # deadline reminders scheduling
    if voting.deadline:
        # TODO: schedule sending of deadline reminder; we need to remember to cancel it if voting changes
        pass
