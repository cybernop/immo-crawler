import logging
from datetime import timedelta

import requests

from immocrawler.provider import listing

logger = logging.getLogger(__name__)


class Client:
    def __init__(self, api_key, travel_locations):
        self.api_key = api_key

        self.travel_locations = []
        for entry in travel_locations:
            loc = listing.Address()
            loc.street = entry['street']
            loc.house_number = entry['house_number']
            loc.post_code = entry['post_code']
            loc.city = entry['city']
            self.travel_locations.append(loc)

    @staticmethod
    def add_links(apartments: listing.Listings):
        logger.info("Adding google maps links")
        n_added = 0
        for _, apartment in apartments.items():
            if apartment.is_valid():
                apartment['google_link'] = f'https://www.google.com/maps/place/{convert_to_string(apartment)}'
                n_added += 1
        logger.info(f"...done for {n_added} entries")

    def add_travel_time(self, apartments):
        logger.info("Adding travel time")
        n_added = 0
        ignore = apartments.deleted
        for _, apartment in apartments.items():
            if apartment.uuid not in ignore and not apartment.travel_times and not apartment.transportation and apartment.address.is_valid():
                travel_times = []
                transits = set()
                for loc in self.travel_locations:
                    travel_time, transit = self.__get_travel_time(loc, apartment.address)
                    if travel_time:
                        travel_times.append(travel_time)
                    if transit:
                        transits.update(transit)
                apartment.travel_times = travel_times
                apartment.transportation = list(transits)
                n_added += 1
                logger.debug(f'added {n_added} entries')
        logger.info(f"...done for {n_added} entries")

    def __get_travel_time(self, origin, destination):
        origin = convert_to_string(origin)
        destination = convert_to_string(destination)

        url = f'https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={self.api_key}&mode=transit'

        r = requests.post(url)
        try:
            legs = r.json()['routes'][0]['legs'][0]
        except (IndexError, KeyError) as e:
            logger.error(f'failed to get transportation legs: {e}')
            duration = None
            transit = None
        else:
            transit = [_get_transport(step) for step in legs['steps']]

            duration = timedelta(seconds=legs['duration']['value'])

        return duration, transit


def _get_transport(step):
    if 'transit_details' in step:
        line = step['transit_details']['line']
        return f'{line["vehicle"]["name"]} {line["short_name"]}'

    return step['travel_mode']


def convert_to_string(loc: listing.Address):
    return ' '.join([loc.street, str(loc.house_number), str(loc.post_code), loc.city]).replace(' ', '+')
