from urllib import urlencode

try:
    import simplejson as json
except :
    import json

from httplib2 import Http

__all__ = [
    'VenueApiClient',
    'MenuItemApiClient',
]

################################################################################

class HttpException(Exception):
    def __init__(self, code, reason, error='Unknown Error'):
        self.code = code
        self.reason = reason
        self.error_message = error
        super(HttpException, self).__init__()

    def __str__(self):        
        return '\n Status: %s \n Reason: %s \n Error Message: %s\n' % (self.code, self.reason, self.error_message)

################################################################################


class HttpApiClient(object):
    """
    Base implementation for an HTTP
    API Client. Used by the different
    API implementation objects to manage
    Http connection.
    """

    def __init__(self, api_key, base_url):
        """Initialize base http client."""
        self.conn = Http()
        # MenuPlatform API key
        self.api_key = api_key
        #base url 
        self.base_url = base_url
        
    def _http_request(self, service_type, **kwargs):
        """
        Perform an HTTP Request using base_url and parameters
        given by kwargs.
        Results are expected to be given in JSON format
        and are parsed to python data structures.
        """
        request_params = urlencode(kwargs)
        request_params = request_params.replace('%28', '').replace('%29', '')

        uri = '%s%s?api_key=%s&%s' % \
            (self.base_url, service_type, self.api_key, request_params)
        header, response = self.conn.request(uri, method='GET')
        return header, response

    def _http_uri_request(self, uri):
        header, response = self.conn.request(uri, method='GET')
        return header, response

    def _is_http_response_ok(self, response):
        return response['status'] == '200' or response['status'] == 200

    def _get_params(self, name = None, category = None, cuisine = None, description = None, price = None, \
                          price__gt = None, price__gte = None, price__lt = None, price__lte = None, \
                          location = (None, None), radius = None, tl_coord = (None, None), \
                          br_coord = (None, None), country = None, locality = None, \
                          region = None, postal_code = None, street_address = None, last_updated = None, \
                          last_updated__gt = None, last_updated__gte = None, last_updated__lt = None, \
                          last_updated__lte = None, website_url = None, dimension = None, has_menu = None, open_at = None):

        lat, long = location
        tl_lat, tl_long = tl_coord
        br_lat, br_long = br_coord

        params = {}
        if name:
            params['name'] = name
        if category:
            if not isinstance(category, list):
                raise TypeError('Please provide list of categories as a category parameter')
            params['category'] = ','.join(category)
        if cuisine:
            if not isinstance(cuisine, list):
                raise TypeError('Please provide list of cuisines as a cuisines parameter')
            params['cuisine'] = ','.join(cuisine)
        if description:
            params['description'] = description
        if price:
            params['price'] = price
        if price__gt:
            params['price__gt'] = price__gt
        if price__gte:
            params['price__gte'] = price__gte
        if price__lt:
            params['price__lt'] = price__lt
        if price__lte:
            params['price__lte'] = price__lte
        if lat and long:
            params['location'] = '%s,%s' % (lat, long) 
            if radius:
                params['radius'] = radius
        if tl_lat and tl_long and br_lat and br_long:
            params['bounds'] = '%s,%s|%s,%s' % (tl_lat, tl_long, br_lat, br_long)
        if country:
            params['country'] = country
        if locality:
            params['locality'] = locality
        if region:
            params['region'] = region
        if postal_code:
            params['postal_code'] = postal_code
        if street_address:
            params['street_address'] = street_address
        if last_updated:
            params['last_updated'] = last_updated
        if last_updated__gt:
            params['last_updated__gt'] = last_updated__gt
        if last_updated__gte:
            params['last_updated__gte'] = last_updated__gte
        if last_updated__lt:
            params['last_updated__lt'] = last_updated__lt
        if last_updated__lte:
            params['last_updated__lte'] = last_updated__lte
        if website_url:
            params['website_url'] = website_url
        if dimension:
            params['dimension'] = dimension
        if has_menu != None:
            params['has_menu'] = has_menu
        if open_at:
            params['open_at'] = open_at
        return params


    def _create_query(self, category_type, params):
        header, content = self._http_request(category_type + '/', **params)
        resp = json.loads(content)
        if not self._is_http_response_ok(header):
            error = resp.get('error_message', 'Unknown Error')
            raise HttpException(header.status, header.reason, error) 
        return resp


################################################################################

class VenueApiClient(HttpApiClient):

    def __init__(self, api_key):
        self.api_url  = 'http://api.locu.com%s'
        base_url = self.api_url % '/v1_0/venue/'
        super(VenueApiClient, self).__init__(api_key, base_url)


    def search(self, category = None, cuisine = None, location = (None, None), radius = None, tl_coord = (None, None), \
                   br_coord = (None, None), name = None, country = None, locality = None, \
                   region = None, postal_code = None, street_address = None, last_updated = None, \
                   last_updated__gt = None, last_updated__gte = None, last_updated__lt = None, \
                   last_updated__lte = None, website_url = None, has_menu = None, open_at = None):
        """
        Locu Venue Search API Call Wrapper

        
        Args: 
        *Note that none of the arguments are required
          category         : List of category types that need to be filtered by: ['restaurant', 'spa', 'beauty salon', 'gym', 'laundry', 'hair care',  'other']
            type : [string]
          cuisine          : List of cuisine types that need to be filtered by: ['american', 'italian', ...]
            type : [string]
          location          : Tuple that consists of (latitude, longtitude) coordinates
            type : tuple(float, float)
          radius            : Radius around the given lat, long
            type : float
          tl_coord          : Tuple that consists of (latitude, longtitude) for bounding box top left coordinates  
            type : tuple(float, float)
          br_coord          : Tuple that consists of (latitude, longtitude) for bounding box bottom right coordinates  
            type : tuple(float, float)
          name              : Name of the venue
            type : string
          country           : Country where venue is located
            type : string
          locality          : Locality. Ex 'San Francisco'
            type : string
          region            : Region/state. Ex. 'CA'
            type : string
          postal_code       : Postal code
            type : string
          street_address    : Address
            type : string
          open_at           : Search for venues open at the specified time
            type : datetime
          last_updated      : A datetime object that scecifies last time venue was updated (ex. 'last_updated=2012-05-06T12:00:00Z')
            type : datetime
          last_updated__gt  : A datetime object that specifies last time venue updated is greater than a given datetime (ex. 'last_updated__gt=2012-05-06T12:00:00Z')  
            type : datetime
          last_updated__gte : A datetime object that specifies last time venue updated is greater than or equal to a given datetime
            type : datetime
          last_updated__lt  : A datetime object that specifies last time venue updated is less than a given datetime
            type : datetime
          last_updated__lte : A datetime object that specifies last time venue updated is less than or equal to a given datetime
            type : datetime
          website_url       : Filter by the a website url
            type : string
          has_menu          : Filter venues that have menus in them
            type : boolean
        Returns:
          A dictionary with a data returned by the server

        Raises:
          HttpException with the error message from the server
        """

        params = self._get_params(category = category, cuisine = cuisine, location = location, radius = radius, tl_coord = tl_coord, \
                                      br_coord = br_coord, name = name, country = country, locality = locality, \
                                      region = region, postal_code = postal_code, street_address = street_address, last_updated = last_updated, \
                                      last_updated__gt = last_updated__gt, last_updated__gte = last_updated__gte, last_updated__lt = last_updated__lt, \
                                      last_updated__lte = last_updated__lte, website_url = website_url, has_menu = has_menu, open_at = open_at)

        return self._create_query('search', params)

    def search_next(self, obj):
        """
        Takes the dictionary that is returned by 'search' or 'search_next' function and gets the next batch of results

        Args: 
          obj: dictionary returned by the 'search' or 'search_next' function

        Returns:
          A dictionary with a data returned by the server

        Raises:
          HttpException with the error message from the server
        """
        if 'meta' in obj and 'next' in obj['meta'] and obj['meta']['next'] != None:
            uri = self.api_url % obj['meta']['next']
            header, content = self._http_uri_request(uri)
            resp = json.loads(content)
            if not self._is_http_response_ok(header):
                error = resp.get('error_message', 'Unknown Error')
                raise HttpException(header.status, header.reason, error) 
            return resp
        return {}

    def insight(self, dimension, category = None, cuisine = None, location = (None, None), radius = None, tl_coord = (None,  None), \
                    br_coord = (None, None), name = None, country = None, locality = None, \
                    region = None, postal_code = None, street_address = None, last_updated = None, \
                    last_updated__gt = None, last_updated__gte = None, last_updated__lt = None, \
                    last_updated__lte = None, website_url = None, has_menu = None, open_at = None):
        """
        Locu Venue Insight API Call Wrapper

        
        Args: 
          REQUIRED:
            dimension         : get insights for a particular dimension. Possible values = {'locality', 'category', 'cuisine', 'region'} 
          OPTIONAL:
            category          : List of category types that need to be filtered by: ['restaurant', 'spa', 'beauty salon', 'gym', 'laundry', 'hair care',  'other']
              type : [string]
            cuisine          : List of cuisine types that need to be filtered by: ['american', 'italian', ...]
              type : [string]
            location          : Tuple that consists of (latitude, longtitude) coordinates
              type : tuple(float, float)
            radius            : Radius around the given lat, long
              type : float
            tl_coord          : Tuple that consists of (latitude, longtitude) for bounding box top left coordinates  
              type : tuple(float, float)
            br_coord          : Tuple that consists of (latitude, longtitude) for bounding box bottom right coordinates  
              type : tuple(float, float)
            name              : Name of the venue
              type : string
            country           : Country where venue is located
              type : string
            locality          : Locality. Ex 'San Francisco'
              type : string
            region            : Region/state. Ex. 'CA'
              type : string
            postal_code       : Postal code
              type : string
            street_address    : Address
              type : string
            open_at           : Search for venues open at the specified time
              type : datetime
            last_updated      : A datetime object that scecifies last time venue was updated (ex. 'last_updated=2012-05-06T12:00:00Z')
              type : datetime
            last_updated__gt  : A datetime object that specifies last time venue updated is greater than a given datetime (ex. 'last_updated__gt=2012-05-06T12:00:00Z')  
              type : datetime
            last_updated__gte : A datetime object that specifies last time venue updated is greater than or equal to a given datetime
              type : datetime
            last_updated__lt  : A datetime object that specifies last time venue updated is less than a given datetime
              type : datetime
            last_updated__lte : A datetime object that specifies last time venue updated is less than or equal to a given datetime
              type : datetime
            website_url       : Filter by the a website url
              type : string
            has_menu          : Filter venues that have menus in them
              type : boolean
        Returns:
          A dictionary with a data returned by the server

        Raises:
          HttpException with the error message from the server
        """

        params =  self._get_params(dimension = dimension, category = category, cuisine = cuisine, location = location, radius = radius, tl_coord = tl_coord, \
                                         br_coord = br_coord, name = name, country = country, locality = locality, \
                                         region = region, postal_code = postal_code, street_address = street_address, last_updated = last_updated, \
                                         last_updated__gt = last_updated__gt, last_updated__gte = last_updated__gte, last_updated__lt = last_updated__lt, \
                                         last_updated__lte = last_updated__lte, website_url = website_url, has_menu = has_menu, open_at = open_at)

        return self._create_query('insight', params)

    def get_details(self, ids):
        """
        Locu Venue Details API Call Wrapper

        Args:
          list of ids : ids of a particular venues to get insights about. Can process up to 5 ids
          

        """
        if isinstance(ids, list):
            if len(ids) > 5:
                ids = ids[:5]
            id_param = ';'.join(ids) + '/'
        else:
            ids = str(ids)
            id_param = ids + '/'

        header, content = self._http_request(id_param)
        print content
        resp = json.loads(content)
        if not self._is_http_response_ok(header):
            error = resp.get('error_message', 'Unknown Error')
            raise HttpException(header.status, header.reason, error) 
        return resp

    def get_menus(self, id):
        """
        Given a venue id returns a list of menus associated with a venue

        """
        resp = self.get_details([id])
        menus = []
        for obj in resp['objects']:
            if obj['has_menu']:
                menus += obj['menus']
        return menus

################################################################################    

class MenuItemApiClient(HttpApiClient):
    def __init__(self, api_key):
        self.api_url  = 'http://api.locu.com%s'
        base_url = self.api_url % '/v1_0/menu_item/'
        super(MenuItemApiClient, self).__init__(api_key, base_url)

    def search(self, name = None, category = None, description = None, price = None, \
                   price__gt = None, price__gte = None, price__lt = None, price__lte = None, \
                   location = (None, None), radius = None, tl_coord = (None, None), \
                   br_coord = (None, None), country = None, locality = None, \
                   region = None, postal_code = None, street_address = None, last_updated = None, \
                   last_updated__gt = None, last_updated__gte = None, last_updated__lt = None, \
                   last_updated__lte = None, website_url = None):
        """
        Locu Menu Item Search API Call Wrapper

        
        Args: 
        *Note that none of the arguments are required
          category          : List of category types that need to be filtered by: ['restaurant', 'spa', 'beauty salon', 'gym', 'laundry', 'hair care',  'other']
            type : [string]
          location          : Tuple that consists of (latitude, longtitude) coordinates
            type : tuple(float, float)
          radius            : Radius around the given lat, long
            type : float
          tl_coord          : Tuple that consists of (latitude, longtitude) for bounding box top left coordinates  
            type : tuple(float, float)
          br_coord          : Tuple that consists of (latitude, longtitude) for bounding box bottom right coordinates  
            type : tuple(float, float)
          name              : Name of the venue
            type : string
          country           : Country where venue is located
            type : string
          locality          : Locality. Ex 'San Francisco'
            type : string
          region            : Region/state. Ex. 'CA'
            type : string
          postal_code       : Postal code
            type : string
          street_address    : Address
            type : string
          last_updated      : A datetime object that scecifies last time venue was updated (ex. 'last_updated=2012-05-06T12:00:00Z')
            type : datetime
          last_updated__gt  : A datetime object that specifies last time venue updated is greater than a given datetime (ex. 'last_updated__gt=2012-05-06T12:00:00Z')  
            type : datetime
          last_updated__gte : A datetime object that specifies last time venue updated is greater than or equal to a given datetime
            type : datetime
          last_updated__lt  : A datetime object that specifies last time venue updated is less than a given datetime
            type : datetime
          last_updated__lte : A datetime object that specifies last time venue updated is less than or equal to a given datetime
            type : datetime
          website_url       : Filter by the a website url
            type : string
          description       : Filter by description of the menu item
            type : string
          price             : get menu items with a particular price value
            type : float
          price__gt         : get menu items with a value greater than particular
            type : float
          price__gte        : greater than or equal
            type : float
          price__lt         : less than
            type : float
          price__lte        : less than or equal
            type : float

        Returns:
          A dictionary with a data returned by the server

        Raises:
          HttpException with the error message from the server
        """

        params =  self._get_params( name = name, description = description, price = price, \
                                       price__gt = price__gt, price__gte = price__gte, price__lt = price__lt, price__lte = price__lte, \
                                       location = location, radius = radius, tl_coord = tl_coord, \
                                       br_coord = br_coord, country = country, locality = locality, \
                                       region = region, postal_code = postal_code, street_address = street_address, last_updated = last_updated, \
                                       last_updated__gt = last_updated__gt, last_updated__gte = last_updated__gte, last_updated__lt = last_updated__lt, \
                                       last_updated__lte = last_updated__lte, website_url = website_url)
        return self._create_query('search', params)

    def search_next(self, obj):
        """
        Takes the dictionary that is returned by 'search' or 'search_next' function and gets the next batch of results

        Args: 
          obj: dictionary returned by the 'search' or 'search_next' function

        Returns:
          A dictionary with a data returned by the server

        Raises:
          HttpException with the error message from the server
        """
        if 'meta' in obj and 'next' in obj['meta'] and obj['meta']['next'] != None:
            uri = self.api_url % obj['meta']['next']
            header, content = self._http_uri_request(uri)
            resp = json.loads(content)
            if not self._is_http_response_ok(header):
                error = resp.get('error_message', 'Unknown Error')
                raise HttpException(header.status, header.reason, error) 
            return resp
        return {}



    def insight(self, dimension, name = None, category = None, description = None, price = None, \
                   price__gt = None, price__gte = None, price__lt = None, price__lte = None, \
                   location = (None, None), radius = None, tl_coord = (None, None), \
                   br_coord = (None, None), country = None, locality = None, \
                   region = None, postal_code = None, street_address = None, last_updated = None, \
                   last_updated__gt = None, last_updated__gte = None, last_updated__lt = None, \
                   last_updated__lte = None, website_url = None):
        """
        Locu Menu Item Insight API Call Wrapper

        
        Args: 
          REQUIRED:
            dimension         : get insights for a particular dimension. Possible values = {'locality', 'region', 'price'}
          OPTIONAL:
            category          : List of category types that need to be filtered by: ['restaurant', 'spa', 'beauty salon', 'gym', 'laundry', 'hair care',  'other']
              type : [string]
            location          : Tuple that consists of (latitude, longtitude) coordinates
              type : tuple(float, float)
            radius            : Radius around the given lat, long
              type : float
            tl_coord          : Tuple that consists of (latitude, longtitude) for bounding box top left coordinates  
              type : tuple(float, float)
            br_coord          : Tuple that consists of (latitude, longtitude) for bounding box bottom right coordinates  
              type : tuple(float, float)
            name              : Name of the venue
              type : string
            country           : Country where venue is located
              type : string
            locality          : Locality. Ex 'San Francisco'
              type : string
            region            : Region/state. Ex. 'CA'
              type : string
            postal_code       : Postal code
              type : string
            street_address    : Address
              type : string
            last_updated      : A datetime object that scecifies last time venue was updated (ex. 'last_updated=2012-05-06T12:00:00Z')
              type : datetime
            last_updated__gt  : A datetime object that specifies last time venue updated is greater than a given datetime (ex. 'last_updated__gt=2012-05-06T12:00:00Z')  
              type : datetime
            last_updated__gte : A datetime object that specifies last time venue updated is greater than or equal to a given datetime
              type : datetime
            last_updated__lt  : A datetime object that specifies last time venue updated is less than a given datetime
              type : datetime
            last_updated__lte : A datetime object that specifies last time venue updated is less than or equal to a given datetime
              type : datetime
            website_url       : Filter by the a website url
              type : string
            description       : Filter by description of the menu item
              type : string
            price             : get menu items with a particular price value
              type : float
            price__gt         : get menu items with a value greater than particular
              type : float
            price__gte        : greater than or equal
              type : float
            price__lt         : less than
              type : float
            price__lte        : less than or equal
              type : float

        Returns:
          A dictionary with a data returned by the server

        Raises:
          HttpException with the error message from the server
        """

        params = self._get_params(name = name, category = category, description = description, price = price, \
                                      price__gt = price__gt, price__gte = price__gte, price__lt = price__lt, price__lte = price__lte, \
                                      location = location, radius = radius, tl_coord = tl_coord, \
                                      br_coord = br_coord, country = country, locality = locality, \
                                      region = region, postal_code = postal_code, street_address = street_address, last_updated = last_updated, \
                                      last_updated__gt = last_updated__gt, last_updated__gte = last_updated__gte, last_updated__lt = last_updated__lt, \
                                      last_updated__lte = last_updated__lte, website_url = website_url, dimension = dimension)
        return self._create_query('insight', params)

    def get_details(self, id):
        """
        Locu MenuItems Details API Call Wrapper

        Args:
          list of ids : ids of a particular menu items to get insights about. Can process up to 5 ids
          

        """
        if isinstance(ids, list):
            if len(ids) > 5:
                ids = ids[:5]
            id_param = ';'.join(ids) + '/'
        else:
            ids = str(ids)
            id_param = ids + '/'

        header, content = self._http_request(id_param)
        resp = json.loads(content)
        if not self._is_http_response_ok(header):
            error = resp.get('error_message', 'Unknown Error')
            raise HttpException(header.status, header.reason, error) 
        return resp

################################################################################
