#!/usr/bin/env python3

import json
import requests 

PCS_HEADER_URL = "https://pcs.baidu.com/rest/2.0/pcs/"

class Session:
    'an interface to the server'
    def __init__(self, access_token, appdir):

        # application directory located under /apps
        self._appdir = appdir
        # absolute path of app directory
        self._fappdir = '/'.join(['/apps', appdir, ''])
        # the session's access token which is required by the server
        self._access_token = access_token

        # initialize the request maker
        self._request_maker = RequestMaker(self._access_token)
    
    # file related operations
    def list(self, path):
        pass

    def move(self, source, dest):
        pass

    def mkdir(self, path):
        pass

    def quota(self):
        return self._request_maker.make_get(PCS_HEADER_URL, 'quota', 'info', {})

    def copy(self, source, dest):
        pass

    # advanced operation provided by Baidu Netdisk

    def offline_download(self):
        pass


class RequestMaker:
    '''request maker helper, for applying request'''
    def __init__(self, access_token):
        self._access_token = access_token

    def make_get(self, header, obj, method, reqs):
        assert type(reqs) == type({})
        reqs['method'] = method
        reqs['access_token'] = self._access_token

        request = requests.get(header + obj, params = reqs)
        return json.loads(request.text)

    def make_post(self, header, obj, method, reqs, data):
        assert type(reqs) == type({})
        reqs['method'] = method
        reqs['access_token'] = self._access_token
        request = requests.post(header + obj, params = reqs, data = data)
        return json.loads(request.text)
