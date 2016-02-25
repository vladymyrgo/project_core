import Cookie
import json
from urllib import urlencode

from tornado import gen
from tornado.httpclient import AsyncHTTPClient, HTTPError
from tornado.options import options


HTTP_CLIENTS = {}


def http_client(scope='default'):
    client = HTTP_CLIENTS.get(scope, None)
    if not client:
        client = AsyncHTTPClient(max_clients=10, force_instance=True)
        HTTP_CLIENTS[scope] = client

    return client


class CommandHandler(object):
    JSON_COMMANDS = set()
    GET_COMMANDS = set()

    def fetch_from_django(self, path, **kwargs):
        """
        Executes an asynchronous HTTP request to project's Django server.
        """
        try:
            return http_client().fetch(options.django + path, **kwargs)
        except HTTPError, e:
            return e

    @gen.engine
    def call_api_command(self, data, callback=None):
        """
        Sends a request to Django server
        """
        res = {}
        # Send a request to Django server
        cookies = Cookie.SimpleCookie()
        if 'sessionid' in data or getattr(self, 'sessionid', None):
            cookies['sessionid'] = data.get('sessionid', None) or self.sessionid
        headers = {'Cookie': cookies.output(header='')}
        host = getattr(self, 'request_host', '')
        # Override request's host
        if host:
            headers['Host'] = host
        cmd = data.pop('cmd', '').replace('.', '/')
        if cmd in self.GET_COMMANDS:
            url = '/api/internal/{}/?{}'.format(cmd, urlencode(data))
            response = yield self.fetch_from_django(url, headers=headers)
        else:
            url = '/api/internal/{}/'.format(cmd)
            if cmd in self.JSON_COMMANDS:
                post_data = json.dumps(data)
            else:
                post_data = urlencode(data)
            response = yield self.fetch_from_django(url,
                                                    headers=headers,
                                                    method='POST',
                                                    body=post_data)
        if response.code == 200:
            try:
                val = json.loads(response.body) or {}
                res.update(val)
            except:
                pass
        if callback:
            callback(res)

    @gen.engine
    def cmd_auth(self, sessionid, callback=None):
        """
        Authenticates user in Django
        """
        # Get the sessionid from the requested data and save it for
        # commands to follow this one
        self.sessionid = sessionid
        # Call the Django server to check if this session valid
        res = yield gen.Task(self.call_api_command, {'cmd': 'auth'})
        # Save a user_id
        self.user_id = res.get('user_id', 0)
        # Subscribe to user's channel
        channels = []
        if self.user_id:
            channels.append('user.%s' % self.user_id)
        if res.get('is_staff', False):
            channels.append('admin.notifications')
        if channels:
            self._subscribe(channels)
        if callback:
            callback(res)
