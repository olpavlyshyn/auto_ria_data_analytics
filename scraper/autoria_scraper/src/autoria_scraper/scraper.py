import asyncio
from .car_details import CarDetails
from functools import wraps


def retry(exceptions, total_tries=4, initial_wait=0.5, backoff_factor=2):
    def retry_decorator(f):
        @wraps(f)
        async def func_with_retries(*args, **kwargs):
            _tries, _delay = total_tries + 1, initial_wait
            while _tries > 1:
                try:
                    return await f(*args, **kwargs)
                except exceptions as e:
                    _tries -= 1
                    print_args = args if args else 'no args'
                    if _tries == 1:
                        msg = str(f'Function: {f.__name__}\n'
                                  f'Failed despite best efforts after {total_tries} tries.\n'
                                  f'args: {print_args}, kwargs: {kwargs}')
                        print(msg)
                        raise
                    msg = str(f'Function: {f.__name__}\n'
                              f'Exception: {e}\n'
                              f'Retrying in {_delay} seconds, args: {print_args}, kwargs: {kwargs}')
                    print(msg)
                    await asyncio.sleep(_delay)
                    _delay += backoff_factor

        return func_with_retries
    return retry_decorator


def parse_car_response(data):
    user_id = data['userId']
    mark_name = data['markName']
    mark_id = data['markId']
    model_name = data['modelName']
    model_id = data['modelId']
    category_name = data['subCategoryName']
    url = data['linkToView']
    state_name = data['stateData']['regionName']
    state_id = data['stateData']['stateId']
    location_name = data['stateData']['name']
    location_id = data['stateData']['cityId']  # test if simillar
    price_usd = data['USD']
    price_uah = data['UAH']
    id = data['autoData']['autoId']
    year = data['autoData']['year']
    vat = data['autoData']['vat']
    mileage = data['autoData']['race']
    fuel = data['autoData']['fuelName']
    gearbox = data['autoData']['gearboxName']
    drive_name = data['autoData']['driveName']
    plate_number = data.get('plateNumber', None)
    vin = data.get('VIN', None)
    have_infotech_report = data['haveInfotechReport']
    auto_info_obj = data['autoInfoBar']
    color_obj = data.get('color', None)
    photo_count = data['photoData']['count']
    main_photo_url = data['photoData']['seoLinkM']
    add_date = data.get('addDate', None)
    update_date = data.get('updateDate', None)
    expire_date = data.get('expireDate', None)
    sold_date = data.get('soldDate', None)
    cd = CarDetails(user_id=user_id, mark_name=mark_name, mark_id=mark_id, model_name=model_name,
                    model_id=model_id, category_name=category_name, url=url, state_name=state_name,
                    state_id=state_id, location_name=location_name, location_id=location_id, price_usd=price_usd,
                    price_uah=price_uah, id=id, year=year, vat=vat, mileage=mileage, fuel=fuel, gearbox=gearbox,
                    drive_name=drive_name, plate_number=plate_number, vin=vin,
                    have_infotech_report=have_infotech_report, auto_info_obj=auto_info_obj,
                    color_obj=color_obj, photo_count=photo_count, main_photo_url=main_photo_url, add_date=add_date, update_date=update_date,
                    expire_date=expire_date, sold_date=sold_date)

    return cd


def generate_search_url(base_url):
    params = {
        "indexName": "auto,order_auto,newauto_search",
        # "body.id[1]": 5,
        "country.import.usa.not": -1,
        "category_id": 1,
        "order_by": 7,
        "custom": 1,  # розмитнені
        "countpage": 100,
    }
    request_url = f"{base_url}/api/search/auto?{'&'.join([k + '=' + str(v) for k, v in params.items()])}"
    return request_url


def generate_car_detail_url(base_url, car_id):
    return f"{base_url}/demo/bu/finalPage/views_auto/{car_id}?lang_id=4"


class AutoRiaScraper:
    BASE_URL = "https://auto.ria.com"

    def __init__(self):
        self.car_list_url = generate_search_url(self.BASE_URL)

    @retry(Exception, total_tries=3)
    async def get_car_ids(self, page_n, session):
        url = f"{self.car_list_url}&page={page_n}"
        r = await session.request(method='GET', url=url)
        response = await r.json()
        ids = response["result"]["search_result"]["ids"]
        if len(ids) != 0:
            return ids

    @retry(Exception, total_tries=3)
    async def get_car_page_async(self, car_id, session):
        url = generate_car_detail_url(self.BASE_URL, car_id)
        r = await session.request(method='GET', url=url)
        if r.status != 503:
            response = await r.json()
            return response

    async def get_cars_data_in_batches_async(self, batch_size, sp, session, deserialize=True):
        cp = sp
        bc = 0
        batch = []
        while True:
            car_ids = await self.get_car_ids(cp, session)
            if not car_ids:
                if len(batch) > 0:
                    yield batch
                break
            results = await asyncio.gather(
                *[self.get_car_page_async(i, session) for i in car_ids],
                return_exceptions=True)
            for data in results:
                if data:
                    if deserialize is True:
                        data = parse_car_response(data)
                    batch.append(data)
            cp = cp + 1
            bc = bc + 1
            if bc == batch_size:
                yield batch
                batch = []
                bc = 0
