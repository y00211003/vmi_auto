#!/usr/bin/env python
# Last modified: 2012-11-16 09:39:09
# Created: 2012-11-16 09:37:44
# Author: Joshua Liu (joshua_liu@trendmicro.com.cn)

"""
Utility to handle URLs.
"""
__author__  = "Joshua Liu (joshua_liu@trendmicro.com.cn)"
__version__ = "$Revision: 0.1 $"
__date__    = "$Date: 2012-11-16 $"

import urllib
import urlparse
import sys

def add_url_params(url, params):
    """Add some params (a mapping object or a sequence of two-element tuples) to a url;
    The order of the params in the result query string will not be changed.
    Return the new url."""
    if params == None:
        return url
    if hasattr(params,"items"):
        # mapping objects
        params = params.items()
    else:
        try:
            if len(params) and not isinstance(params[0], tuple):
                # not list of tuples
                raise TypeError
        except TypeError:
            ty,va,tb = sys.exc_info()
            raise TypeError, "not a valid non-string sequence or mapping object", tb
    for k,v in params:
        if k is None or v is None:
            params.remove((k, v)) # skip the None key
    url_parts = list(urlparse.urlparse(url))
    query = urlparse.parse_qsl(url_parts[4], keep_blank_values=1)
    query.extend(params)
    url_parts[4] = urllib.urlencode(query)
    return urlparse.urlunparse(url_parts)

class QueryParams(object):
    def __init__(self, params={}):
        if params is None: params = {}
        self.params = dict(params)

    def add_param(self, field_name, value=''):
        if value is None:
            #value = ''
            raise ValueError('None value is not allowed')
        self.params[field_name] = value

    def remove_param(self, field_name):
        if self.params.has_key(field_name):
            self.params.pop(field_name)

    def clear(self):
        self.params.clear()

    def to_query_string(self):
        return urllib.urlencode(self.params)

