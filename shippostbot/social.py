from requests import Request, Response, Session

from . import log


class FacebookPage(object):
    pass


class Facebook(object):
    def __init__(self,
                 access_token: str,
                 api_version: str = 'v3.3'):
        self.access_token = access_token
        self.api_version = api_version
        self.session = Session()

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

    def get_user(self, user_id: str = None) -> FacebookPage:
        return FacebookPage(self, user_id)


class FacebookUser(object):
    def __init__(self, root: Facebook, user_id: str = None):
        self.root = root
        self.user_id = user_id
        self.logger = log.create_logger(FacebookUser)
    
    def post(self, path, **kwargs) -> Response:
        endpoint = self.get_user_endpoint()
        return self.root.post('%s/%s' % (endpoint, path), **kwargs)

    def publish_photo(self, caption: str, image_url: str) -> Response:
        self.logger.info('Publishing photo, caption: %s, image url: %s' % (caption, image_url))
        return self.post('photos', params={
            'caption': caption,
            'url': image_url
        })

    def get_user_endpoint(self) -> str:
        return self.user_id if self.user_id is not None else 'me'
