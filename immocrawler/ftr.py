import logging
from datetime import timedelta

from immocrawler.provider import listing

logger = logging.getLogger(__name__)


class Filter:
    def __init__(self, config):
        self.config = config

    def filter_title(self, listings: listing.Listings):
        logger.info('filter title...')
        remove_uuids = []
        try:
            for uuid, entry in listings.items():
                if self.__should_remove_title(entry):
                    remove_uuids.append(uuid)
                    continue

            for uuid in remove_uuids:
                listings.remove_entry(uuid)

            logger.info(f'...removed {len(remove_uuids)} entries')
        except KeyError:
            logger.warning(f'could not filter as entry is missing in config')

    def __should_remove_title(self, entry: listing.Entry):
        return any(title_word.lower() in entry.title.lower() for title_word in self.config['title_words'])

    def filter_post_code(self, listings: listing.Listings):
        logger.info('filter post code...')
        remove_uuids = []
        try:
            for uuid, entry in listings.items():
                if self.__should_remove_post_code(entry):
                    remove_uuids.append(uuid)
                    continue

            for uuid in remove_uuids:
                listings.remove_entry(uuid)

            logger.info(f'...removed {len(remove_uuids)} entries')
        except KeyError:
            logger.warning(f'could not filter as entry is missing in config')

    def __should_remove_post_code(self, entry: listing.Entry):
        return int(entry.address.post_code) not in self.config['post_code']

    def filter_price(self, listings: listing.Listings):
        logger.info('filter price...')
        remove_uuids = []
        try:
            for uuid, entry in listings.items():
                if self.__should_remove_price(entry):
                    remove_uuids.append(uuid)
                    continue

            for uuid in remove_uuids:
                listings.remove_entry(uuid)

            logger.info(f'...removed {len(remove_uuids)} entries')
        except KeyError:
            logger.warning(f'could not filter as entry is missing in config')

    def __should_remove_price(self, entry: listing.Entry):
        price_span = self.config['price_warm']

        if 'min' in price_span and entry.price_warm < price_span['min']:
            return True

        if 'max' in price_span and entry.price_warm > price_span['max']:
            return True

        return False

    def filter_living_space(self, listings: listing.Listings):
        logger.info('filter living space...')
        remove_uuids = []
        try:
            for uuid, entry in listings.items():
                if self.__should_remove_living_space(entry):
                    remove_uuids.append(uuid)
                    continue

            for uuid in remove_uuids:
                listings.remove_entry(uuid)

            logger.info(f'...removed {len(remove_uuids)} entries')
        except KeyError:
            logger.warning(f'could not filter as entry is missing in config')

    def __should_remove_living_space(self, entry: listing.Entry):
        span = self.config['living_space']

        if 'min' in span and entry.living_space < span['min']:
            return True

        if 'max' in span and entry.living_space > span['max']:
            return True

        return False

    def filter_travel_time(self, listings: listing.Listings):
        logger.info('filter travel time...')
        remove_uuids = []
        try:
            for uuid, entry in listings.items():
                if self.__should_remove_travel_time(entry):
                    remove_uuids.append(uuid)
                    continue

            for uuid in remove_uuids:
                listings.remove_entry(uuid)

            logger.info(f'...removed {len(remove_uuids)} entries')
        except KeyError:
            logger.warning(f'could not filter as entry is missing in config')

    def __should_remove_travel_time(self, entry: listing.Entry):
        span = self.config['travel_time']
        min = timedelta(minutes=span['min']) if 'min' in span else None
        max = timedelta(minutes=span['max']) if 'max' in span else None

        for travel_time in entry.travel_times:
            if min and travel_time < min:
                return True

            if max and travel_time > max:
                return True

        return False
