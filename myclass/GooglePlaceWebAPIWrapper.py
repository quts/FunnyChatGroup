import requests, time, json
from urllib.parse import urlencode, quote_plus

class GooglePlaceWebAPIWrapper(object):
    
    def __init__(self, key):
        self._key = key
        self._keyword = 'restaurant'
        self._radius=500

    def get(self,latitude,longitude):
        url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
        params = {
            'location' : '%s,%s'%(latitude,longitude),
            'radius'   : self._radius,
            'keyword'  : self._keyword,
            'key'      : self._key
        }
        
        # Get json data
        obj_page = requests.get(url, params=params)

        if obj_page.ok:
            json_resp = json.loads(obj_page.text)
            return json_resp['results']

class GoogleStaticMapsAPIWrapper(object):

    def __init__(self, key = None, url = None):
        self._key      = key
        self._base_url = url

    def get(self,latitude,longitude,place_name, token):
#        url = 'https://maps.googleapis.com/maps/api/staticmap'
        url = self._base_url
        params = {
            'center'   : '%s,%s'%(latitude,longitude),
            'zoom'     : 15,
            'size'     : '600x632',
            'language' : 'zh-tw',
            'markers'  : r'size:mid|color:red|' + '%s'%place_name,
            'token'    : token
        }
        params_string = urlencode(params, quote_via=quote_plus)
        #obj_page = requests.get(url, params=params)

        return '%s?%s'%(url, params_string)


if __name__ == '__main__':
    GooglePlaceWebAPIWrapper(GLOBALS.GOOGLE_SERVICES_API_KEY).get('25.023235208374818','121.548479385674')