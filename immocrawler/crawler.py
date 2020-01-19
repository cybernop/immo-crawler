import logging
import pathlib

import yaml

from immocrawler import provider, ftr
from immocrawler.inout import cache

CACHE_FILE_NAME = 'cache'

logger = logging.getLogger(__name__)


class Crawler:

    def __init__(self, config, data_dir='.', notifier=None, gmaps_client=None):
        self.config = config
        self.data_dir = pathlib.Path(data_dir).absolute()
        self.cache_file = self.data_dir / CACHE_FILE_NAME
        self.notifier = notifier
        self.gmaps_client = gmaps_client

        self.filter = ftr.Filter(config['filters'])

    def crawl(self):
        apartments = cache.read(self.cache_file)

        apartments_new = provider.get_apartments(self.config['providers'])

        self.filter.filter_post_code(apartments_new)
        self.filter.filter_living_space(apartments_new)
        self.filter.filter_price(apartments_new)

        updated = apartments.update(apartments_new)
        removed = apartments.remove_not_existing(apartments_new)
        logging.getLogger().info(f"got {len(updated)} updates, removed {removed}")

        # googlemaps.add_gmaps_link(apartments)
        self.gmaps_client.add_travel_time(apartments)

        self.filter.filter_travel_time(apartments)

        try:
            if self.notifier and len(updated) > 0:
                notification = f'got {len(updated)} updates, removed {removed}'
                self.notifier.send_message(notification)
                entries = self.get_updated_entries(apartments, updated)

                for entry in entries:
                    self.notifier.send_message(str(entry))
        except Exception as e:
            logger.error(f'failed to send notifications: {e}')

        cache.write(apartments, self.cache_file)

    @staticmethod
    def get_updated_entries(apartments, updated):
        updated_entries = []
        for update in updated:
            try:
                entry = getattr(apartments, update.uuid)
                updated_entries.append(entry)
            except AttributeError:
                logger.debug(f'ignore removed entry {update.uuid}')
        return updated_entries


if __name__ == '__main__':
    def main():
        logging.basicConfig(level=logging.INFO)

        with open("configs/config.yml", 'r') as yml_file:
            cfg = yaml.load(yml_file, Loader=yaml.SafeLoader)

        crawler = Crawler(cfg)
        crawler.crawl()


    main()
