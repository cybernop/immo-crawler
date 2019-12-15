class Entry:
    __slots__ = ['uuid', 'id', 'mod_date', 'title', 'living_space', 'number_of_rooms', 'balcony', 'garden', 'built_in_kitchen', 'private', 'price_base', 'price_warm', 'source', 'url', 'address', 'contact']

    def __init__(self):
        self.uuid = None
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

    def __getattr__(self, item: str):
        if item not in self.map:
            return None
        return self.map[item]

    def __setattr__(self, key: str, value: Entry):
        self.map[key] = value

    def __getstate__(self):
        return self.map

    def __setstate__(self, state):
        super(Listings, self).__setattr__('map', state)

    def __len__(self):
        return len(self.map)

    def update(self, other):
        updated = []
        for uuid, app in other.map.items():
            if uuid in self.map:
                if app.mod_date > self.map[uuid].mod_date:
                    self.map[uuid] = app
                    updated.append(app)
            else:
                setattr(self, uuid, app)
                updated.append(app)
        return updated
