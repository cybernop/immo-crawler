import logging
import requests


def get_apartments(config, cfg):
    logger = logging.getLogger(__name__)
    logger.info("Getting information from immobilienscout24.de")

    list_ = {}
    for district in cfg['districts']:
        logger.info(f"for {district}...")
        list_[district] = _get_apartments(cfg['state'], cfg['city'], district, config)
        logger.info(f"...got {len(list_[district])} entries")
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
        results += [__make_nice_entry(x['resultlist.realEstate']) for x in entries]

        i += 1

        if 'next' not in result_list['paging']:
            break
    return results


def __format_for_url(num):
    return '{:.2f}'.format(num).replace(".", ",") if num != 0 else ""


def __make_nice_entry(entry):
    result = {
        'title': entry['title'],
        'apartment_postcode': entry['address']['postcode'],
        'apartment_city': entry['address']['city'],
        'apartment_quarter': entry['address']['quarter'],
        'living_space': entry['livingSpace'],
        'number_of_rooms': entry['numberOfRooms'],
        'balcony': entry['balcony'],
        'garden': entry['garden'],
        'built_in_kitchen': entry['builtInKitchen'],
        'private': entry['privateOffer'],
        'price_base': entry['price']['value'],
        'price_warm': entry['calculatedPrice']['value'],
    }

    if 'firstname' in entry['contactDetails']:
        result['contact_firstname'] = entry['contactDetails']['firstname']

    if 'lastname' in entry['contactDetails']:
        result['contact_lastname'] = entry['contactDetails']['lastname']

    if 'cellPhoneNumber' in entry['contactDetails']:
        result['contact_phone_number'] = entry['contactDetails']['cellPhoneNumber']
    elif 'phoneNumber' in entry['contactDetails']:
        result['contact_phone_number'] = entry['contactDetails']['phoneNumber']

    if 'street' in entry['address']:
        result['apartment_street'] = entry['address']['street']
    if 'houseNumber' in entry['address']:
        result['apartment_houseNumber'] = entry['address']['houseNumber']

    if 'company' in entry['contactDetails']:
        result['contact_company'] = entry['contactDetails']['company']

    result['source'] = 'immobilienscout24'
    result['id'] = 'https://www.immobilienscout24.de/expose/' + entry['@id']

    return result
