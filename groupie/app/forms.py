# -*- coding: utf-8 -*-
from datetime import datetime

from django import forms
from django.core.validators import validate_email

from groupie.app.models import Voting, Voter, VotingOption


class MultiEmailField(forms.Field):
    def _parse_emails(self, emails):
        """
        Expects emails as a comma separated list of emails (can also contain one email).
        """
        return [e.strip() for e in emails.split(',')]

    def to_python(self, value):
        "Normalize data to a list of strings."

        # Return an empty list if no input was given.
        if not value:
            return []
        return self._parse_emails(value)

    def validate(self, value):
        "Check if value consists only of valid emails."

        # Use the parent's handling of required fields, etc.
        super(MultiEmailField, self).validate(value)

        for email in value:
            validate_email(email)


class VotingAddForm(forms.ModelForm):
    emails = MultiEmailField()

    class Meta:
        model = Voting
        # TODO: handle 'deadlint' and 'voting_options' properly
        exclude = ('deadline', 'voting_options')

    def clean(self, *args, **kwargs):
        cleaned_data = super(VotingAddForm, self).clean(*args, **kwargs)

        # manually cleaning deadline
        d = self.data.get('deadline')
        if d:
            d = datetime.strptime(d, '%d/%m/%Y %H:%M').strftime('%Y-%m-%d %H:%M')
            cleaned_data.update({'deadline': d})

        # manually cleaning voting options
        vos = self.data.getlist('voting_options')
        if not vos:
            self._errors["voting_options"] = ["Voting options missing"]
        cleaned_data.update({'voting_options': vos})

        # removing creator from invited
        emails = [e for e in self.cleaned_data.get('emails', []) if not e == self.cleaned_data['from_email']]
        if not emails:
            self._errors["emails"] = ["This field is required"]
        cleaned_data.update({'emails': emails})

        # TODO: check if deadline is not later then the closest option
        return cleaned_data

    def save(self, *args, **kwargs):
        emails = self.cleaned_data.pop('emails')
        voting_options = self.cleaned_data.pop('voting_options')

        v = Voting.objects.create(**self.cleaned_data)
        for e in emails:
            Voter.objects.create(voting=v, email=e)
        for vo in voting_options:
            VotingOption.objects.create(voting=v, text=vo)

        return v
