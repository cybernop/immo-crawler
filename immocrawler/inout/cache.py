import logging
import pathlib
import pickle

from immocrawler.provider import listing

logger = logging.getLogger(__name__)


def write(data, file_name):
    logging.info(f"Writing {len(data)} entries")
    pathlib.Path(file_name).write_bytes(pickle.dumps(data))


def read(file_name):
    file = pathlib.Path(file_name)
    if file.exists():
        data = pickle.loads(file.read_bytes())
        logging.info(f"Read {len(data)} entries")
        return data
    return listing.Listings()
