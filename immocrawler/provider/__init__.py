import pathlib

from immocrawler.provider import listing

pwd = pathlib.Path(__file__).parent


def get_apartments(config):
    ignore = ['listing', '__init__']

    apartments = listing.Listings()
    for child in pwd.iterdir():
        if child.is_file() and child.stem not in ignore and child.suffix == '.py' and not child.stem.startswith("test_"):
            name = child.stem
            imported = getattr(__import__('immocrawler.provider', fromlist=[name]), name)
            res = imported.get_apartments(config, config.providers[name])
            apartments.update(res)
    return apartments
