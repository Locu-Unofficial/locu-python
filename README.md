locu-python
===========

This is unofficial Locu API wrapper.

# Installation
git clone https://github.com/Locu/locu-python.git locu-python

# Usage
from locu.api import VenueApiClient, MenuItemApiClient

## Venue API

```python
venue_client = VenueApiClient(KEY)
```

### Get venues in San Francisco locality
```python
venues = venue_client.search(locality = 'San Francisco')
```

### Get venues in CA with 'italian' in the venue name
```python
venues2 = venue_client.search(region = 'CA', name = 'italian')
```

### Get next 25 search results for the previous query

Note that this is only available for special partners.

```python
more_venues = venue_client.search_next(venues2)
```

### Get insights for data
```python
venue_insights = venue_client.insight(dimension = 'category', location = (37.775, -122.4183)
```

### Get more details for particular venues. 
```python
details = venue_client.get_details(['715b3fc8c0798faf91ae', 'a8fbe449987c9e8150c8'])
```

### Get menus for a particular venue
```python
venue_menus = venue_client.get_menus('715b3fc8c0798faf91ae')
```

## Menu Item API
```python
from locu import MenuItemApiClient
menu_item_client = MenuItemApiClient(KEY)
menu_items = menu_item_client.search(locality = 'San Francisco', name = 'espresso', price__gte = 6)  
print menu_items['objects'][0]
```
### Menu Item Insight 
from locu import MenuItemApiClient
menu_item_client = MenuItemApiClient(KEY)    
v_c.insight(dimension = 'price', locality = 'San Francisco', name = 'pizza')
