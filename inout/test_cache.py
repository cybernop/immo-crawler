import pathlib

from inout import cache
from provider import listing

from unittest import TestCase

file = pathlib.Path('testdump').absolute()


class TestCache(TestCase):
    def setUp(self):
        if file.exists():
            file.unlink()
        self.assertFalse(file.exists())

    def tearDown(self):
        if file.exists():
            file.unlink()
        self.assertFalse(file.exists())

    def test_write_read(self):
        entry = listing.Entry()
        entry.id = '123'

        cache.write(entry, str(file))
        self.assertTrue(file.exists())

        entry_read = cache.read(str(file))
        self.assertEqual(entry.id, entry_read.id)
