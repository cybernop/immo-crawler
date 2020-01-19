import logging
import pathlib

import yaml

from immocrawler import provider, googlemaps
from immocrawler.inout import cache

CACHE_FILE_NAME = 'cache'


class Config:
    def __init__(self):
        self.min_price = 0
        self.max_price = 0
        self.min_size = 0
        self.max_size = 0
        self.min_rooms = 0
        self.max_rooms = 0
        self.providers = {}


class Crawler:

    def __init__(self, config, data_dir='.', notifier=None, gmaps_client=None):
        self.config = config
        self.data_dir = pathlib.Path(data_dir).absolute()
        self.cache_file = self.data_dir / CACHE_FILE_NAME
        self.notifier = notifier
        self.gmaps_client = gmaps_client

    def crawl(self):
        apartments = cache.read(self.cache_file)

        apartments_new = provider.get_apartments(self.config)

        updated = apartments.update(apartments_new)
        removed = apartments.remove_not_existing(apartments_new)
        logging.getLogger().info(f"got {len(updated)} updates, removed {removed}")

        # googlemaps.add_gmaps_link(apartments)
        self.gmaps_client.add_travel_time(apartments)

        if self.notifier and len(updated) > 0:
            notification = f'got {len(updated)} updates, removed {removed}'
            self.notifier.send_message(notification)
            entries = self.get_updated_entries(apartments, updated)

            for entry in entries:
                self.notifier.send_message(str(entry))

        cache.write(apartments, self.cache_file)

    @staticmethod
    def get_updated_entries(apartments, updated):
        return [getattr(apartments, update.uuid) for update in updated]


if __name__ == '__main__':
    def main():
        logging.basicConfig(level=logging.INFO)

        with open("configs/config.yml", 'r') as yml_file:
            cfg = yaml.load(yml_file, Loader=yaml.SafeLoader)

        config = Config()
        config.min_size = 60
        config.min_price = 500
        config.max_price = 1500
        config.providers = cfg['providers']

        crawler = Crawler(config)
        crawler.crawl()


    main()
