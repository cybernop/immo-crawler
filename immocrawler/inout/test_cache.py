import pathlib

from immocrawler.inout import cache
from immocrawler.provider import listing

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

        cache.write([entry], str(file))
        self.assertTrue(file.exists())

        entries_read = cache.read(str(file))
        self.assertEqual(1, len(entries_read))
        self.assertEqual(entry.id, entries_read[0].id)
