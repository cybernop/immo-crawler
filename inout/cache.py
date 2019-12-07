import logging
import pathlib
import pickle

logger = logging.getLogger(__name__)


def write(data, file_name):
    info = data.info()
    logging.info(f"Writing {info['quarters']} quarters with {info['entries']} entries")
    pathlib.Path(file_name).write_bytes(pickle.dumps(data))


def read(file_name):
    file = pathlib.Path(file_name)
    if file.exists():
        data = pickle.loads(file.read_bytes())
        info = data.info()
        logging.info(f"Writing {info['quarters']} quarters with {info['entries']} entries")
        return data
    return {}
