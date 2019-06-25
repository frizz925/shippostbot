from __future__ import annotations

import json

from requests import Request, Response, Session

from ..log import create_logger

DEFAULT_API_VERSION = 'v3.3'


class Facebook(object):
    def __init__(self,
                 access_token: str,
                 api_version: str = DEFAULT_API_VERSION,
                 session: Session = None):
        self.access_token = access_token
        self.api_version = api_version
        self.session = session if session is not None else Session()
        self.logger = create_logger(Facebook)

    def get_endpoint(self) -> str:
        return 'https://graph.facebook.com/%s' % self.api_version

    def request(self, method: str, path: str, **kwargs) -> Response:
        url = '%s/%s' % (self.get_endpoint(), path)
        kwargs['headers'] = self.get_headers(kwargs.get('headers'))
        kwargs['params'] = self.get_params(kwargs.get('params'))
        req = Request(method=method, url=url, **kwargs)
        prep = req.prepare()
        return self.session.send(prep)

    def get(self, path: str, **kwargs) -> Response:
        return self.request('GET', path, **kwargs)

    def post(self, path: str, **kwargs) -> Response:
        return self.request('POST', path, **kwargs)

    def get_headers(self, headers=None) -> dict:
        if headers is None:
            headers = {}
        return dict({
            'User-Agent': 'ShippostBot'
        }, **headers)

    def get_params(self, params=None) -> dict:
        if params is None:
            params = {}
        return dict({
            'access_token': self.access_token
        }, **params)

    def get_user(self, user_id: str = None) -> FacebookUser:
        return FacebookUser(self, user_id)

    def publish_comment(self, post_id: str, message: str) -> Response:
        self.logger.info('publish_comment(%s)' % json.dumps({'post_id': post_id, 'message': message}))
        return self.post('%s/comments' % post_id, params={
            'message': message
        })


class FacebookUser(object):
    def __init__(self, root: Facebook, user_id: str = None):
        self.root = root
        self.user_id = user_id
        self.logger = create_logger(FacebookUser)

    def post(self, path, **kwargs) -> Response:
        endpoint = self.get_user_endpoint()
        return self.root.post('%s/%s' % (endpoint, path), **kwargs)

    def publish_photo(self, caption: str, image_url: str) -> Response:
        self.logger.info('publish_photo(%s)' % json.dumps({'caption': caption, 'image_url': image_url}))
        return self.post('photos', params={
            'caption': caption,
            'url': image_url
        })

    def get_user_endpoint(self) -> str:
        return self.user_id if self.user_id is not None else 'me'
