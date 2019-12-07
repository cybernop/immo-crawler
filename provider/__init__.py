import pathlib

from provider import listing

pwd = pathlib.Path(__file__).parent


def get_apartments(config, cfg):
    ignore = ['listing', '__init__']

    apartments = listing.Listings()
    for child in pwd.iterdir():
        if child.is_file() and child.stem not in ignore and child.suffix == '.py':
            name = child.stem
            imported = getattr(__import__('provider', fromlist=[name]), name)
            res = imported.get_apartments(config, cfg[name])
            apartments += res
    return apartments
