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
        return self._request_maker.make_get(PCS_HEADER_URL, 'file', 'list',
                {'path' : self._to_abs_path(path)})

    def meta(self, path):
        'obtain the meta data of a given file'
        return self._request_maker.make_get(PCS_HEADER_URL, 'file', 'meta',
                {'path' : self._to_abs_path(path)})

    def move(self, source, dest):
        'move a file from source to the destination'
        return self._request_maker.make_post(PCS_HEADER_URL, 'file', 'move', {},
                {'from' : self._to_abs_path(source), 
                 'to'   : self._to_abs_path(dest)})

    def mkdir(self, path):
        'create a new directory'
        return self._request_maker.make_post(PCS_HEADER_URL, 'file', 'mkdir', 
                {'path' : self._to_abs_path(path)}, {})

    def quota(self):
        'return the quota information of your netdisk'
        return self._request_maker.make_get(PCS_HEADER_URL, 'quota', 'info', {})

    def copy(self, source, dest):
        'copy a file or directory from the source to the destination'
        return self._request_maker.make_post(PCS_HEADER_URL, 'file', 'copy', {},
                {'from' : self._to_abs_path(source),
                 'to'   : self._to_abs_path(dest)})

    # advanced operation provided by Baidu Netdisk

    def offline_download(self):
        pass

    # helper function
    def _to_abs_path(self, path):
        return '/'.join([self._fappdir, path])


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
