# -*- coding: utf-8 -*-
from django.forms import ModelForm

from groupie.app.models import Voting


class VotingForm(ModelForm):
    class Meta:
        model = Voting
