import requests

from .endpoints import ENDPOINTS
from .exceptions import InvalidURLException


class OsuAPI():
    """A simple api wrapper. Not all endpoints are implemented.
    Every public method takes a dict as its argument, mapping keys to values."""

    def __init__(self, key):
        """Initializes an API instance."""
        self._key = key
        self.base_url = "https://osu.ppy.sh/api/{}?k=" + self._key

    def _check_parameters(self, ep, params):
        """Checks that all parameters required by the endpoint are present in the passed arguments,
        and that all passed arguments are possible parameters for the endpoint."""
        for required in ep.REQUIRED:
            if(required not in params):
                raise InvalidURLException("{} is a required argument for {}".format(required, ep.EXTENSION))

        for key in params:
            if(key not in ep.POSSIBLE):
                raise InvalidURLException("{} cannot be set for {}".format(key, ep.EXTENSION))

    def _extend_url(self, url, params):
        """Adds every key/value pair in the params dict to the url."""
        # filter out None parameters
        params = {k:v for k,v in params if k is not None}
        for key in params:
            url = url + "&{}={}".format(key, params[key])
        return url

    def _process_url(self, url):
        """Makes a request to the osu api and returns the json response."""
        return requests.get(url).json()

    def get_scores(self, params):
        """Retrieves score data about the leaderboards of a map."""
        ep = ENDPOINTS.GET_SCORES
        self._check_parameters(ep, params)
        url = self.base_url.format(ep.EXTENSION)
        url = self._extend_url(url, params)
        return self._process_url(url)

    def get_replay(self, params):
        """Retrieves replay data by a user on a map."""
        ep = ENDPOINTS.GET_REPLAY
        self._check_parameters(ep, params)
        url = self.base_url.format(ep.EXTENSION)
        return self._extend_url(url, params)