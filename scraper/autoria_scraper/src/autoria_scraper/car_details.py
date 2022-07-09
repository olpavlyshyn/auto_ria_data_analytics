def get_schema(separator):
    output = ['id', 'user_id', 'mark_name', 'mark_id', 'model_name', 'model_id', 'category_name', 'url', 'state_name', 'state_id',
                'location_name', 'location_id', 'year', 'price_usd', 'price_uah', 'vat', 'mileage', 'fuel', 'gearbox', 'plate_number',
                'drive_name', 'vin', 'have_infotech_report',  'auto_info_obj', 'color_obj', 'photo_count', 'main_photo_url',
                'add_date', 'update_date', 'expire_date', 'sold_date']
    return separator.join([str(o) for o in output])


class CarDetails:
    def __init__(self, id, user_id, mark_name, mark_id, model_name, model_id, category_name, url, state_name, state_id,
                 location_name, location_id, year, price_usd, price_uah, vat, mileage, fuel, gearbox, plate_number,
                 drive_name, vin, have_infotech_report,  auto_info_obj, color_obj, photo_count, main_photo_url,
                 add_date, update_date, expire_date, sold_date):
        self.id = id
        self.user_id = user_id

        self.mark_name = mark_name
        self.mark_id = mark_id
        self.model_name = model_name
        self.model_id = model_id
        self.category_name = category_name

        self.url = url # linkToView

        self.state_name = state_name # regionName
        self.state_id = state_id
        self.location_name = location_name
        self.location_id = location_id

        self.year = year

        self.price_usd = price_usd
        self.price_uah = price_uah
        self.vat = vat
        self.mileage = mileage #race
        self.fuel = fuel
        self.gearbox = gearbox
        self.drive_name = drive_name

        self.auto_info_obj = auto_info_obj

        self.color_obj = color_obj
        self.photo_count = photo_count
        self.main_photo_url = main_photo_url

        self.mileage = mileage
        self.plate_number = plate_number

        self.vin = vin
        self.have_infotech_report = have_infotech_report

        self.add_date = add_date
        self.update_date = update_date
        self.expire_date = expire_date
        self.sold_date = sold_date

    def serialize(self, separator):
        output = [self.id, self.user_id, self.mark_name, self.mark_id, self.model_name, self.model_id, self.category_name,
                  self.url, self.state_name, self.state_id, self.location_name, self.location_id, self.year, self.price_usd,
                  self.price_uah, self.vat, self.mileage, self.fuel, self.gearbox, self.plate_number, self.drive_name,
                  self.vin, self.have_infotech_report,  self.auto_info_obj, self.color_obj, self.photo_count, self.main_photo_url,
                  self.add_date, self.update_date, self.expire_date, self.sold_date]
        return separator.join([str(o) for o in output])
