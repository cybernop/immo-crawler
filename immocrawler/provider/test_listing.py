import unittest
from datetime import datetime

from immocrawler.provider import listing


class TestListingsUpdate(unittest.TestCase):

    def test_empty(self):
        listings1 = listing.Listings()
        self.assertEqual(0, len(listings1), 'listing1 not empty at beginning')

        listings2 = listing.Listings()
        self.assertEqual(0, len(listings2), 'listing2 not empty at beginning')

        update = listings1.update(listings2)
        self.assertEqual(0, len(update), 'update is not empty')
        self.assertEqual(0, len(listings1), 'listing1 not in original state')

    def test_update_empty(self):
        entry = listing.Entry()
        entry.id = 'foobar'
        entry.mod_date = datetime.now()

        listings1 = listing.Listings()
        listings1.foo = entry
        self.assertEqual(1, len(listings1), 'listing1 does not contain entry at beginning')

        listings2 = listing.Listings()
        self.assertEqual(0, len(listings2), 'listing2 not empty at beginning')

        update = listings1.update(listings2)
        self.assertEqual(0, len(update), 'update is not empty')
        self.assertEqual(1, len(listings1), 'listing1 not in original state')

    def test_no_overlap(self):
        entry1 = listing.Entry()
        entry1.id = 'foobar1'
        entry1.mod_date = datetime.now()

        listings1 = listing.Listings()
        listings1.foo1 = entry1
        self.assertEqual(1, len(listings1), 'listing1 does not contain entry at beginning')

        entry2 = listing.Entry()
        entry2.id = 'foobar2'
        entry2.mod_date = datetime.now()

        listings2 = listing.Listings()
        listings2.foo2 = entry2
        self.assertEqual(1, len(listings2), 'listing2 does not contain entry at beginning')

        update = listings1.update(listings2)
        self.assertEqual(1, len(update), 'update should contain one entry')
        self.assertEqual(2, len(listings1), 'listing1 does not contain both entries')

    def test_one_update(self):
        entry1 = listing.Entry()
        entry1.id = 'foobar1'
        entry1.mod_date = datetime.now()

        listings1 = listing.Listings()
        listings1.foo = entry1
        self.assertEqual(1, len(listings1), 'listing1 does not contain entry at beginning')

        entry2 = listing.Entry()
        entry2.id = 'foobar2'
        entry2.mod_date = datetime.now()

        listings2 = listing.Listings()
        listings2.foo = entry2
        self.assertEqual(1, len(listings2), 'listing1 does not contain entry at beginning')

        update = listings1.update(listings2)
        self.assertEqual(1, len(update), 'update should contain one entry')
        self.assertEqual(1, len(listings1), 'listings1 should contain one entry')
        self.assertEqual(entry2.id, listings1.foo.id)


class TestListingsRemove(unittest.TestCase):

    def test_empty(self):
        listings1 = listing.Listings()
        listings1_len = len(listings1)
        self.assertEqual(0, listings1_len, 'listing1 not empty at beginning')

        listings2 = listing.Listings()
        self.assertEqual(0, len(listings2), 'listing2 not empty at beginning')

        removed = listings1.remove_not_existing(listings2)
        self.assertEqual(0, len(removed), 'number of removed entries does not match')
        self.assertEqual(listings1_len - len(removed), len(listings1), 'remaining number of entries does not match')

    def test_no_remove(self):
        entry = listing.Entry()
        entry.mod_date = datetime.now()

        listings1 = listing.Listings()
        listings1.foo = entry
        listings1_len = len(listings1)
        self.assertEqual(1, listings1_len, 'listing1 does not contain entry at beginning')

        listings2 = listing.Listings()
        listings2.foo = entry
        self.assertEqual(1, len(listings2), 'listing2 does not contain entry at beginning')

        removed = listings1.remove_not_existing(listings2)
        self.assertEqual(0, len(removed), 'number of removed entries does not match')
        self.assertEqual(listings1_len - len(removed), len(listings1), 'remaining number of entries does not match')

    def test_remove(self):
        entry = listing.Entry()
        entry.mod_date = datetime.now()

        listings1 = listing.Listings()
        listings1.foo = entry
        listings1_len = len(listings1)
        self.assertEqual(1, listings1_len, 'listing1 does not contain entry at beginning')

        listings2 = listing.Listings()
        self.assertEqual(0, len(listings2), 'listing2 not empty at beginning')

        removed = listings1.remove_not_existing(listings2)
        self.assertEqual(1, len(removed), 'number of removed entries does not match')
        self.assertEqual(listings1_len - len(removed), len(listings1), 'remaining number of entries does not match')


if __name__ == '__main__':
    unittest.main()
