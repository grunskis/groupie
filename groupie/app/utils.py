# -*- coding: utf-8 -*-
import os
from urllib import urlencode

from django.core.urlresolvers import reverse


BASE_URL = os.environ.get('BASE_URL', 'http://localhost:8000')


def get_abs_url(voting, referer):
    voting_url = reverse('voting', args=[voting.url_hash])
    qs = urlencode({'ref': referer})
    return '{}{}?{}'.format(BASE_URL, voting_url, qs)
