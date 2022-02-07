from datetime import datetime
from dataclasses import dataclass


@dataclass
class CarDetails:
    brand: str = None
    model: str = None
    year: int = None
    url: str = None
    currency: str = None
    price: float = None
    mileage: str = None
    location: str = None
    fuel: str = None
    gearbox: str = None
    checked_vin: str = None
    checked_num: str = None
    accident: str = None
    created: datetime = None
    modified: datetime = None
    sold: datetime = None

    def serialize(self, separator):
        output = (self.brand, self.model, self.year, self.url, self.currency, self.price, self.mileage, self.location,
                  self.fuel, self.gearbox, self.checked_vin, self.checked_num, self.accident, self.created,
                  self.modified, self.sold)
        return separator.join([str(o) for o in output])
