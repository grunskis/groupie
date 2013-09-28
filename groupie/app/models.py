# -*- coding: utf-8 -*-
import random
import string

from django.db import models


## VOTING ##

def generate_hash():
    while True:
        url_hash = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        if not Voting.objects.filter(url_hash=url_hash).exists():
            return url_hash


class Voting(models.Model):
    url_hash = models.CharField(primary_key=True, max_length=8, default=generate_hash, editable=False)

    from_email = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField(blank=True, null=True)

    # start an email discussion
    send_to_all = models.BooleanField()

    def __unicode__(self):
        """
        Returns a snapshot of current scores.
        """
        # TODO: makes some smart aggregation here
        # and basically check all other places where related managers are called...
        scores = ["{} [{}]".format(o, o.voters.count()) for o in self.voting_options.all()]
        return u', '.join(scores)

    @property
    def creator(self):
        return self.voters.get(email=self.from_email)


## VOTING OPTION ##

class VotingOption(models.Model):
    voting = models.ForeignKey(Voting, related_name='voting_options')

    text = models.CharField(max_length=255)

    def __unicode__(self):
        return u'{}'.format(self.text)


## VOTER ##


def generate_ref():
    while True:
        ref_hash = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        if not Voter.objects.filter(ref_hash=ref_hash).exists():
            return ref_hash


class Voter(models.Model):
    voting = models.ForeignKey(Voting, related_name='voters')
    voted_voting_options = models.ManyToManyField(VotingOption, related_name='voters')

    ref_hash = models.CharField(primary_key=True, max_length=8, default=generate_ref, editable=False)
    email = models.EmailField()

    def __unicode__(self):
        return u'{}'.format(self.email)
