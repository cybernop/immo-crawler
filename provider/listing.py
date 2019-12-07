class Entry:
    __slots__ = ['id', 'mod_date', 'title', 'living_space', 'number_of_rooms', 'balcony', 'garden', 'built_in_kitchen', 'private', 'price_base', 'price_warm', 'source', 'url', 'address', 'contact']

    def __init__(self):
        self.id = None
        self.mod_date = None
        self.title = None
        self.living_space = None
        self.number_of_rooms = None
        self.balcony = None
        self.garden = None
        self.built_in_kitchen = None
        self.private = None
        self.price_base = None
        self.price_warm = None
        self.source = None
        self.url = None
        self.address = None
        self.contact = None


class Address:
    __slots__ = ['street', 'house_number', 'post_code', 'quarter', 'city']

    def __init__(self):
        self.street = None
        self.house_number = None
        self.post_code = None
        self.quarter = None
        self.city = None


class Contact:
    __slots__ = ['company', 'first_name', 'last_name', 'mobile_phone', 'phone']

    def __init__(self):
        self.company = None
        self.first_name = None
        self.last_name = None
        self.mobile_phone = None
        self.phone = None


class Listings:
    def __init__(self):
        super(Listings, self).__setattr__('map', {})

    def __getattr__(self, item):
        if item not in self.map:
            self.map[item] = []
        return self.map[item]

    def __setattr__(self, key, value):
        self.map[key] = value

    def __add__(self, other):
        for quarter, aps in other.map.items():
            new = getattr(self, quarter) + aps
            setattr(self, quarter, new)
        return self

    def __getstate__(self):
        return self.map

    def __setstate__(self, state):
        super(Listings, self).__setattr__('map', state)

    def info(self):
        entries = 0
        for _, list_ in self.map.items():
            entries += len(list_)
        return {'quarters': len(self.map), 'entries': entries}
