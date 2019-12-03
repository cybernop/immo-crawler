from datetime import datetime
import logging
import requests

from provider import listing


def get_apartments(config, cfg):
    logger = logging.getLogger(__name__)
    logger.info("Getting information from immobilienscout24.de")

    list_ = {}
    for label, district in cfg['districts'].items():
        logger.info(f"for {label}...")
        list_[label] = _get_apartments(cfg['state'], cfg['city'], district, config)
        logger.info(f"...got {len(list_[label])} entries")
    logger.info("...done")

    return list_


def _get_apartments(state, city, district, config):
    min_price = __format_for_url(config.min_price)
    max_price = __format_for_url(config.max_price)
    min_rooms = __format_for_url(config.min_rooms)
    max_rooms = __format_for_url(config.max_rooms)
    min_size = __format_for_url(config.min_size)
    max_size = __format_for_url(config.max_size)

    i = 1
    results = []
    while True:
        url = f'https://www.immobilienscout24.de/Suche/S-T/P-{i}/Wohnung-Miete/{state}/{city}/{district}/{min_rooms}-{max_rooms}/{min_size}-{max_size}/EURO-{min_price}-{max_price}/-/-/-/true/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/2,3'

        r = requests.post(url)
        result_list = r.json()['searchResponseModel']['resultlist.resultlist']
        entries = result_list['resultlistEntries'][0]['resultlistEntry']
        results += [__make_entry(x) for x in entries]

        i += 1

        if 'next' not in result_list['paging']:
            break
    return results


def __format_for_url(num):
    return '{:.2f}'.format(num).replace(".", ",") if num != 0 else ""


def __make_entry(entry_dict):
    entry = listing.Entry()

    entry.id = entry_dict['@id']
    entry.mod_date = datetime.strptime(entry_dict['@modification'].replace(':', ''), '%Y-%m-%dT%H%M%S.%f%z')

    entry_dict = entry_dict['resultlist.realEstate']

    entry.title = entry_dict['title']
    entry.living_space = entry_dict['livingSpace']
    entry.number_of_rooms = entry_dict['numberOfRooms']
    entry.balcony = entry_dict['balcony']
    entry.garden = entry_dict['garden']
    entry.built_in_kitchen = entry_dict['builtInKitchen']
    entry.private = entry_dict['privateOffer']
    entry.price_base = entry_dict['price']['value']
    entry.price_warm = entry_dict['calculatedPrice']['value']

    entry.source = 'immobilienscout24'
    entry.url = 'https://www.immobilienscout24.de/expose/' + entry_dict['@id']

    address_dict = entry_dict['address']
    address = listing.Address()

    address.street = address_dict.get('street')
    address.house_number = address_dict.get('houseNumber')
    address.quarter = address_dict['quarter']
    address.post_code = address_dict['postcode']
    address.city = address_dict['city']

    entry.address = address

    contact_dict = entry_dict['contactDetails']
    contact = listing.Contact()

    contact.first_name = contact_dict.get('firstname')
    contact.last_name = contact_dict.get('lastname')
    contact.mobile_phone = contact_dict.get('cellPhoneNumber')
    contact.phone = contact_dict.get('phoneNumber')
    contact.company = contact_dict.get('company')

    entry.contact = contact

    return entry
