# -*- coding: utf-8 -*-
from django import forms
from django.core.validators import validate_email

from groupie.app.models import Voting


class MultiEmailField(forms.Field):
    def to_python(self, value):
        "Normalize data to a list of strings."

        # Return an empty list if no input was given.
        if not value:
            return []
        return Voting.parse_emails(value)

    def validate(self, value):
        "Check if value consists only of valid emails."

        # Use the parent's handling of required fields, etc.
        super(MultiEmailField, self).validate(value)

        for email in value:
            validate_email(email)


class MultiOptionsField(forms.Field):
    def to_python(self, value):
        "Normalize data to a list of strings."

        # Return an empty list if no input was given.
        if not value:
            return []
        return Voting.parse_options(value)


class VotingForm(forms.ModelForm):
    emails = MultiEmailField()
    options = MultiOptionsField()

    class Meta:
        model = Voting

    def save(self, *args, **kwargs):
        # FIXME
#         v = Voting.objects.create(**voting_dict)
#         for e in Voting.parse_emails(emails):
#             Voter.objects.create(voting=v, email=e)
#         for o in Voting.parse_options(options):
#             VotingOption.objects.create(voting=v, text=o)
#         return v
        pass
