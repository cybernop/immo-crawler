import argparse
import logging
import pathlib
import time

import yaml

import immocrawler.crawler as cwlr
import immocrawler.notifier as ntfr


def main():
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('--data-dir', default='.', help='directory where to store data')
    arg_parser.add_argument('--config', required=True, help='config yaml file')

    args = arg_parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    if not pathlib.Path(args.config).exists():
        logging.error(f'config file does not exist {args.config}')
        exit(-1)

    with open(args.config, 'r') as yml_file:
        cfg = yaml.load(yml_file, Loader=yaml.SafeLoader)

    config = cwlr.Config()
    config.min_size = 60
    config.min_price = 500
    config.max_price = 1500
    config.providers = cfg['providers']

    notifier = ntfr.Notifier(name=cfg['notifier']['name'], greeting=cfg['notifier']['greeting'], token=cfg['notifier']['token'])

    crawler = cwlr.Crawler(config, args.data_dir, notifier)
    while True:
        crawler.crawl()
        time.sleep(cfg['update_interval'])


if __name__ == '__main__':
    main()
