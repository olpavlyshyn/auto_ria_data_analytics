from bs4 import BeautifulSoup
import requests
from logger import AutoRiaScrapLogger
from car_details import CarDetails


def generate_search_url(base_url):
    params = {
        "indexName": "auto,order_auto",
        # "body.id[1]": 5,
        "country.import.usa.not": -1,
        # "price.USD.gte": min_price,
        # "price.USD.lte": max_price,
        "custom.not": 1,  # розмитнені
        "size": 100,
        # "page":1
    }
    request_url = f"{base_url}/search?{'&'.join([k + '=' + str(v) for k, v in params.items()])}"
    print(request_url)
    return request_url


def parse_ticket(ticket):
    cd = CarDetails()
    hidden_div = ticket.find("div", class_="hide")
    cd.brand = hidden_div["data-mark-name"]
    cd.model = hidden_div["data-model-name"]
    cd.year = hidden_div["data-year"]
    cd.url = ticket.find("a", class_="address")["href"]
    price_ticket = ticket.find("div", class_="price-ticket")
    cd.currency, cd.price = price_ticket["data-main-currency"], price_ticket["data-main-price"]

    characteristic = ticket.find("ul", class_="characteristic")
    list_items = characteristic.find_all("li")
    cd.mileage, cd.location, cd.fuel, cd.gearbox = [i.text.strip() for i in list_items]
    if cd.location[-7:] == "( від )":
        cd.location = cd.location[:-8]

    base_information = ticket.find("div", class_="base_information")
    cd.checked_vin = None
    if base_information.find("span", class_="label-vin") is not None:
        cd.checked_vin = True
    elif base_information.find("span", class_="vin-code") is not None:
        cd.checked_vin = False
    cd.checked_num = None
    if base_information.find("span", class_="state-num") is not None:
        cd.checked_num = True
    cd.accident = False
    if base_information.find("span", string="Був в ДТП") is not None:
        cd.accident = True

    footer_ticket = ticket.find("div", class_="footer_ticket")
    footer_span = footer_ticket.find("span")

    cd.created, cd.modified, cd.sold = None, None, None
    if footer_span.get("data-sold-date") is None:
        cd.created, cd.modified = footer_span["data-add-date"], footer_span["data-update-date"]
    else:
        cd.sold = footer_span["data-sold-date"]
    return cd


def save_to_file(folder, category, file_index, data, log):
    file_path = f'{folder}/{category}_07-02-2022/{category}_{file_index}.csv'
    with open(file_path, "a") as f:
        f.write('\n'.join([d.serialize(";") for d in data]))
        print(f"saved {len(data)} rows to {file_path}.")
    log.add_file_save_log(file_path, len(data))


class AutoRiaScraper:
    BASE_URL = "https://auto.ria.com/uk"

    def __init__(self):
        # self.url = generate_search_url(self.BASE_URL)
        self.url = "https://auto.ria.com/uk/legkovie/citroen/c4-cactus/?&page=0"

    def get_page(self, page_number):
        r = requests.get(f"{self.url}&page={page_number}")
        return r.content

    def get_cars_data(self):
        current_page = 0
        while True:
            content = self.get_page(current_page)
            soup = BeautifulSoup(content, "html.parser")
            items = soup.find_all("section", class_="ticket-item")
            cars_data = []
            if len(items) == 0:
                break
            for i in items:
                car = parse_ticket(i)
                cars_data.append(car)
            yield cars_data, current_page
            current_page = current_page + 1

    def save(self, folder, category):
        log = AutoRiaScrapLogger(r"C:/projects/AutoRia/scraper")
        log.add_header(self.url)
        file_index = 1
        data = []
        for page, page_number in scraper.get_cars_data():
            data = data + page
            log.add_page_read_log(page_number, len(page))
            if file_index % 10 == 0:
                save_to_file(folder, category, file_index, data, log)
                file_index = file_index + 1
                data = []
        if len(data) > 0:
            save_to_file(folder, category, file_index, data, log)
        log.close()


if __name__ == '__main__':
    scraper = AutoRiaScraper()
    scraper.save(r"C:/projects/AutoRia/data", "CACTUS")
