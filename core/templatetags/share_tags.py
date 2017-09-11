from django import template

import os
from urllib.parse import urlparse, parse_qsl, urlunparse, urlencode

register = template.Library()

@register.simple_tag
def get_facebook_share(**kwargs):

    host = os.path.join('http://', kwargs['host'])
    print(host)
    page_uri = kwargs['page']
    image = kwargs.get('image', '')
    summary = kwargs.get('summary', '')
    title = kwargs.get('title', '')
    base_link = 'https://facebook.com/sharer/sharer.php?s=100'

    url_parts = list(urlparse(base_link))
    query = dict(parse_qsl(url_parts[4]))
    params = {
        'p[url]': os.path.join(host, page_uri[:1]),
        'p[images][0]': os.path.join(host, image[:1]),
        'p[title]': title,
        'p[summary]': summary
    }

    query.update(params)

    url_parts[4] = urlencode(query)
    print(urlunparse(url_parts))
    return urlunparse(url_parts)

@register.filter
def get_twitter_share(item, likelist):
    return likelist.exist_item(item)

@register.filter
def get_pinterest_share(item, likelist):
    return ''

@register.filter
def get_mail_share(item, likelist):
    return ''