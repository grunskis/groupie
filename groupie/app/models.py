# -*- coding: utf-8 -*-
import string
import random

from django.db import models


## VOTING ##

def generate_hash():
    while True:
        url_hash = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        if not Voting.objects.filter(url_hash=url_hash).exists():
            return url_hash


def parse_emails(emails):
    """
    Expects emails as a comma separated list of emails (can also contain one email).
    """
    return [e.strip() for e in emails.split(',')]


def parse_options(options):
    """
    Expects voting options as a # separated list of options (can also contain one email).
    """
    return [o.strip() for o in options.split('#')]


def create_voting(emails, options, voting_dict):
    # TODO: for testing purposes; should be in form probably
    v = Voting.objects.create(**voting_dict)
    for e in parse_emails(emails):
        Voter.objects.create(voting=v, email=e)
    for o in parse_options(options):
        VotingOption.objects.create(voting=v, text=o)
    return v


class Voting(models.Model):
    url_hash = models.CharField(primary_key=True, max_length=8, default=generate_hash, editable=False)

    from_email = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()

    # indicates if want to send notification emails to all emails at once (as one group email)
    send_to_all = models.BooleanField()

    def __unicode__(self):
        """
        Returns a snapshot of current scores.
        """
        # TODO: makes some smart aggregation here
        scores = ["{} [{}]".format(o, o.voters.count()) for o in self.voting_options.all()]
        return u', '.join(scores)


## VOTING OPTION ##

class VotingOption(models.Model):
    voting = models.ForeignKey(Voting, related_name='voting_options')

    text = models.CharField(max_length=255)

    def __unicode__(self):
        return u'{}'.format(self.text)


## VOTER ##


def vote(voter, option):
    # TODO: for testing purposes; should be in form probably
    option.voters.add(voter)


def generate_ref():
    while True:
        url_ref = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        if not Voter.objects.filter(url_ref=url_ref).exists():
            return url_ref


class Voter(models.Model):
    voting = models.ForeignKey(Voting, related_name='voters')
    options = models.ManyToManyField(VotingOption, related_name='voters')

    url_ref = models.CharField(primary_key=True, max_length=8, default=generate_ref, editable=False)
    email = models.EmailField()

    def __unicode__(self):
        return u'{}'.format(self.email)

# from datetime import datetime, timedelta
# from groupie.app.models import create_voting
# 
# emails = "a@a.com, b@b.com"
# options = "1 # 2 # foo"
# voting_dict = {
#     'from_email': "foo@foo.bar",
#     'description': "foobar",
#     'deadline': datetime.now() + timedelta(seconds=10),
#     'send_to_all': True
# }
# 
# v = create_voting(emails, options, voting_dict)
# 
# 
# ###
# 
# from groupie.app.models import vote
# 
# 
# vrs = v.voters.all()
# os = v.voting_options.all()
# 
# vote(vrs[0], os[0])
# 
# v   
