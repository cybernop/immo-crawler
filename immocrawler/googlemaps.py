import logging
from typing import List

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
        for _, apartment in apartments.items():
            if not apartment.travel_times and apartment.address.is_valid():
                travel_times = []
                for loc in self.travel_locations:
                    travel_times.append(self.__get_travel_time(loc, apartment.address))
                apartment.travel_times = travel_times
                n_added += 1
                logger.debug(f'added {n_added} entries')
        logger.info(f"...done for {n_added} entries")

    def __get_travel_time(self, origin, destination):
        origin = convert_to_string(origin)
        destination = convert_to_string(destination)

        url = f'https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={self.api_key}&mode=transit'

        r = requests.post(url)
        return r.json()['routes'][0]['legs'][0]['duration']['text']


def convert_to_string(loc: listing.Address):
    return ' '.join([loc.street, str(loc.house_number), str(loc.post_code), loc.city]).replace(' ', '+')
