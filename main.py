import logging
import pandas
import yaml

import provider
import googlemaps
from inout import cache


class Config:
    def __init__(self):
        self.min_price = 0
        self.max_price = 0
        self.min_size = 60
        self.max_size = 0
        self.min_rooms = 0
        self.max_rooms = 0


def main(cache_file):
    logging.basicConfig(level=logging.INFO)

    apartments = cache.read(cache_file)

    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.SafeLoader)

    config = Config()
    config.min_price = 500
    config.max_price = 1500

    apartments_new = provider.get_apartments(config, cfg['providers'])

    updated = apartments.update(apartments_new)
    removed = apartments.remove_not_existing(apartments_new)
    logging.getLogger().info(f"got {len(updated)} updates, removed {removed}")

    # googlemaps.add_gmaps_link(apartments)
    # add_travel_time(cfg['google'], apartments)
    # write_to_excel('results.xlsx', apartments]

    cache.write(apartments, cache_file)


def add_travel_time(google_cfg, apartments):
    googlemaps.add_travel_time(apartments, google_cfg)


def write_to_excel(file_name, apartments):
    with pandas.ExcelWriter(file_name) as writer:
        for quarter, aps in apartments.items():
            data_frame = _to_data_frame(aps)
            data_frame.to_excel(writer, sheet_name=quarter)
        writer.save()


def snake_to_camel(word):
    return ''.join(x.capitalize() or '_' for x in word.split('_'))


def _to_data_frame(apartments):
    data_frame = pandas.DataFrame.from_dict(apartments)
    data_frame.columns = map(snake_to_camel, data_frame.columns)
    return data_frame


if __name__ == '__main__':
    cache_file = 'cache'

    main(cache_file)
