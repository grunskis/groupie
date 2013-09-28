# -*- coding: utf-8 -*-
from django.shortcuts import render

from groupie.app.forms import VotingForm


def home(request):
    form = VotingForm()
    return render(request, 'home.html', {'form': form})
