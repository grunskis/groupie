# -*- coding: utf-8 -*-
import string
import random

from django.db import models


def generate_hash():
    # Brutus Forcus
    while True:
        url_hash = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        if not Voting.objects.filter(url_hash=url_hash).exists():
            return url_hash


class Voting(models.Model):
    url_hash = models.CharField(primary_key=True, max_length=8, default=generate_hash, editable=False)

    from_email = models.CharField(max_length=255)
    to_emails = models.TextField()  # expects ',' separated values

    description = models.TextField()
    options = models.TextField()  # expects '#' separated values
    deadline = models.DateTimeField()

    # indicates if want to send notification emails to all emails at once (as one group email)
    send_to_all = models.BooleanField()
