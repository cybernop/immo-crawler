import logging
import pandas
import yaml

import provider
import googlemaps


class Config:
    def __init__(self):
        self.min_price = 0
        self.max_price = 0
        self.min_size = 60
        self.max_size = 0
        self.min_rooms = 0
        self.max_rooms = 0


def main():
    logging.basicConfig(level=logging.INFO)

    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.SafeLoader)

    config = Config()
    config.min_price = 500
    config.max_price = 1500

    apartments = provider.get_apartments(config, cfg['providers'])
    googlemaps.add_gmaps_link(apartments)
    add_travel_time(cfg['google'], apartments)
    write_to_excel('results.xlsx', apartments)


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
    main()
