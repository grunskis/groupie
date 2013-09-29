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
    url_hash = models.CharField(primary_key=True, max_length=8,
                                default=generate_hash, editable=False)
    from_email = models.EmailField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField(blank=True, null=True)

    notify_create_at = models.DateTimeField(blank=True, null=True)
    notify_deadline_at = models.DateTimeField(blank=True, null=True)
    notify_half_voted_at = models.DateTimeField(blank=True, null=True)
    notify_all_voted_at = models.DateTimeField(blank=True, null=True)

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

    @property
    def description_short(self, length=50):
        short = self.description[:50]
        return u"{}...".format(short)


## VOTING OPTION ##

class VotingOption(models.Model):
    voting = models.ForeignKey(Voting, related_name='voting_options')

    option = models.DateTimeField()

    def __unicode__(self):
        return unicode(self.option)


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
