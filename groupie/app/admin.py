# -*- coding: utf-8 -*-
from django.contrib import admin

from groupie.app.models import Voting, VotingOption, Voter


admin.site.register(Voting)
admin.site.register(Voter)
admin.site.register(VotingOption)
