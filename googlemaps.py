import logging
import requests


logger = logging.getLogger(__name__)


def add_gmaps_link(apartments):
    logger.info("Adding google maps links")
    n_added = 0
    for quarter in apartments.values():
        for apartment in quarter:
            if location_valid(apartment):
                apartment['google_link'] = f'https://www.google.com/maps/place/{convert_to_string(apartment)}'
                n_added += 1
    logger.info(f"...done for {n_added} entries")


def add_travel_time(apartments, cfg):
    logger.info("Adding travel time")
    n_added = 0
    for quarter in apartments.values():
        for apartment in quarter:
            if location_valid(apartment):
                for name, loc in cfg['travel_locations'].items():
                    apartment[name] = get_travel_time(loc, apartment, cfg['api_key'])
                n_added += 1
    logger.info(f"...done for {n_added} entries")


def location_valid(loc):
    return 'apartment_street' in loc and 'apartment_houseNumber' in loc and 'apartment_postcode' in loc and 'apartment_city' in loc


def get_travel_time(origin, destination, api_key):
    origin = convert_to_string(origin)
    destination = convert_to_string(destination)

    url = f'https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={api_key}&mode=transit'

    r = requests.post(url)
    return r.json()['routes'][0]['legs'][0]['duration']['text']


def convert_to_string(loc):
    return ' '.join([loc['apartment_street'], str(loc['apartment_houseNumber']), str(loc['apartment_postcode']),
                     loc['apartment_city']]).replace(' ', '+')
