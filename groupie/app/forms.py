# -*- coding: utf-8 -*-
import pytz
from datetime import datetime

from django import forms
from django.conf import settings
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
        exclude = ('deadline', 'voting_options')

    def _parse_datetime(self, dt):
        naive = datetime.strptime(dt, '%d/%m/%Y %H:%M')
        return pytz.timezone(settings.TIME_ZONE).localize(naive)

    def clean(self, *args, **kwargs):
        cleaned_data = super(VotingAddForm, self).clean(*args, **kwargs)

        # manually cleaning voting options
        vos = [self._parse_datetime(x) for x in self.data.getlist('voting_options') if x]
        if not vos:
            self._errors["voting_options"] = ["Voting options missing"]
        cleaned_data.update({'voting_options': vos})

        # manually cleaning deadline
        d = self.data.get('deadline')
        if d:
            d = self._parse_datetime(d)
            if max(d, *vos) == d:
                self._errors["deadline"] = ["Deadline must be before last option."]
            cleaned_data.update({'deadline': d.strftime('%Y-%m-%d %H:%M')})

        # removing creator from invited
        emails = [e for e in self.cleaned_data.get('emails', []) if not e == self.cleaned_data.get('from_email')]
        if not emails:
            self._errors["emails"] = ["This field is required"]
        cleaned_data.update({'emails': emails})

        return cleaned_data

    def save(self, *args, **kwargs):
        emails = self.cleaned_data.pop('emails')
        voting_options = self.cleaned_data.pop('voting_options')

        v = Voting.objects.create(**self.cleaned_data)

        for e in emails:
            Voter.objects.create(voting=v, email=e)

        # voting creator is also added as a voter
        Voter.objects.create(voting=v, email=v.from_email)

        for vo in voting_options:
            VotingOption.objects.create(voting=v, option=vo)

        return v


class VotingForm(forms.ModelForm):
    options = forms.MultipleChoiceField(
        required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = VotingOption
        fields = ('options',)

    def __init__(self, *args, **kwargs):
        voting = kwargs.pop('voting')

        super(VotingForm, self).__init__(*args, **kwargs)

        options = voting.voting_options.values_list('id', 'option')
        self.fields['options'].choices = options
