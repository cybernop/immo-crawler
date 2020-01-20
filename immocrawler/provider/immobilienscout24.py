from datetime import datetime
import logging
import requests

from immocrawler.provider import listing

logger = logging.getLogger(__name__)


def get_apartments(provider_config):
    logger.info("Getting information from immobilienscout24.de")

    logger.info(f"for {provider_config['city']}...")
    listings = _get_apartments(provider_config['state'], provider_config['city'])
    logger.info(f"...got {len(listings)} entries")

    return listings


def _get_apartments(state, city):
    i = 1
    results = listing.Listings()
    while True:
        url = f'https://www.immobilienscout24.de/Suche/S-T/P-{i}/Wohnung-Miete/{state}/{city}/-/-/-/-/-/-/-/true/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/2,3'

        r = requests.post(url)
        result_list = r.json()['searchResponseModel']['resultlist.resultlist']
        entries = result_list['resultlistEntries'][0]['resultlistEntry']

        for entry in entries:
            try:
                entry = __make_entry(entry)
            except Exception as e:
                logger.error(f'failed to create entry: {e}')
            else:
                setattr(results, entry.uuid, entry)

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

    entry.uuid = f"{entry.source}-{entry.id}"

    return entry
