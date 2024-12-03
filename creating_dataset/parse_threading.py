import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import time

SAVE_PATH = "data"

os.chdir(os.path.dirname(__file__))
if not os.path.isdir(SAVE_PATH):
    os.makedirs(SAVE_PATH)

with open("headers") as f:
    headers = {header.split(": ")[0]: header.split(": ")[1] for header in f.read().strip().split("\n")}


def fetch_count(price_from, price_to, km_from=0, km_to=1_000_000):
    def get_params(price_from, price_to, km_from=0, km_to=1_000_000):
        return {
            "price_from": price_from,
            "price_to": price_to,
            "km_age_from": km_from,
            "km_age_to": km_to,
            "section": "used",
            "category": "cars",
            "output_type": "list",
            "geo_id": [225],
            "sort": "cr_date-desc",
        }

    url = "https://auto.ru/-/ajax/desktop-search/listingCount/"

    response = requests.post(url, json=get_params(price_from, price_to, km_from, km_to), headers=headers).json()
    return response["pagination"]["total_page_count"]


def fetch_offers(price_from, price_to, km_from=0, km_to=1_000_000):
    def get_params(price_from, price_to, page, km_from=0, km_to=1_000_000):
        return {
            "price_from": price_from,
            "price_to": price_to,
            "km_age_from": km_from,
            "km_age_to": km_to,
            "section": "used",
            "category": "cars",
            "output_type": "list",
            "geo_id": [225],
            "sort": "cr_date-desc",
            "page": page,
        }

    url = "https://auto.ru/-/ajax/desktop-search/listing/"

    pages = fetch_count(price_from, price_to, km_from, km_to)

    if pages >= 99 and price_to - price_from == 1:
        diff = (km_to - km_from) // 2
        fetch_offers(price_from, price_to, km_from, km_to - diff)
        fetch_offers(price_from, price_to, km_from + diff, km_to)
        return

    elif pages >= 99:
        diff = (price_to - price_from) // 2
        fetch_offers(price_from, price_to - diff)
        fetch_offers(price_from + diff, price_to)
        return

    print(f"{price_from} - {price_to}, {km_from} - {km_to}", pages, end="\n")
    if pages <= 0:
        return

    for page in range(1, pages + 1):
        errors = 0
        while True:
            try:
                response = requests.post(url, json=get_params(price_from, price_to, page, km_from, km_to), headers=headers)
                data = response.json()
                offers = [convert_offer(i) for i in data["offers"]]
                if len(offers) == 0:
                    break
                with open(os.path.join(SAVE_PATH, f"data_{price_from}_{price_to}_{km_from}_{km_to}_{page}.json"), "w", encoding="utf8") as f:
                    json.dump(offers, f, ensure_ascii=False)
                break

            except Exception as e:
                if errors > 3:
                    break
                print(e)
                time.sleep(10)
                errors += 1


def convert_offer(offer: dict):
    def safe_get(d: dict, keys: list, default=None):
        for key in keys:
            d = d.get(key, {})
        return d if d else default

    return {
        "owners": safe_get(offer, ["documents", "owners_number"], "None"),
        "year": safe_get(offer, ["documents", "year"], "None"),
        "price": safe_get(offer, ["price_info", "price"], "None"),
        "region": str(safe_get(offer, ["seller", "location"], {})),
        "mileage": safe_get(offer, ["state", "mileage"], "None"),
        "body_type": {"type": safe_get(offer, ["vehicle_info", "configuration", "body_type"], "None"), "name": safe_get(offer, ["vehicle_info", "configuration", "human_name"], "None")},
        "mark": safe_get(offer, ["vehicle_info", "mark_info", "name"], "None"),
        "model": safe_get(offer, ["vehicle_info", "model_info", "name"], "None"),
        "super_gen": {"name": safe_get(offer, ["vehicle_info", "super_gen", "name"], "None"), "from": safe_get(offer, ["vehicle_info", "super_gen", "year_from"], "None"), "to": safe_get(offer, ["vehicle_info", "super_gen", "year_to"], "None")},
        "complectation": safe_get(offer, ["vehicle_info", "complectation", "name"], "None"),
        "steering_wheel": safe_get(offer, ["vehicle_info", "steering_wheel"], "None"),
        "gear_type": safe_get(offer, ["vehicle_info", "tech_param", "gear_type"], "None"),
        "engine": safe_get(offer, ["vehicle_info", "tech_param", "engine_type"], "None"),
        "transmission": safe_get(offer, ["vehicle_info", "tech_param", "transmission"], "None"),
        "power": safe_get(offer, ["vehicle_info", "tech_param", "power"], "None"),
        "displacement": safe_get(offer, ["vehicle_info", "tech_param", "displacement"], "None"),
        "characteristics": safe_get(offer, ["vehicle_info", "tech_param", "human_name"], "None"),
        "color": offer.get("color_hex", "None"),
    }


def convert_offer_old(offer: dict):
    return {
        "owners": offer.get("documents", {}).get("owners_number", "None"),
        "year": offer.get("documents", {}).get("year", "None"),
        "price": offer.get("price_info", {}).get("price", "None"),
        "region": str(offer.get("seller", {}).get("location", {})),
        "condition": offer.get("state", {}).get("condition", "None"),
        "mileage": offer.get("state", {}).get("mileage", "None"),
        "doors": offer.get("vehicle_info", {}).get("configuration", {}).get("doors_count", "None"),
        "class": offer.get("vehicle_info", {}).get("configuration", {}).get("auto_class", "None"),
        "body_type": offer.get("vehicle_info", {}).get("configuration", {}).get("body_type", "None"),
        "mark": offer.get("vehicle_info", {}).get("mark_info", {}).get("name", "None"),
        "model": offer.get("vehicle_info", {}).get("model_info", {}).get("name", "None"),
        "super_gen": offer.get("vehicle_info", {}).get("super_gen", {}).get("name", "None"),
        "steering_wheel": offer.get("vehicle_info", {}).get("steering_wheel", "None"),
        "gear_type": offer.get("vehicle_info", {}).get("tech_param", {}).get("gear_type", "None"),
        "engine": offer.get("vehicle_info", {}).get("tech_param", {}).get("engine_type", "None"),
        "transmission": offer.get("vehicle_info", {}).get("tech_param", {}).get("transmission", "None"),
        "power": offer.get("vehicle_info", {}).get("tech_param", {}).get("power", "None"),
        "displacemnt": offer.get("vehicle_info", {}).get("tech_param", {}).get("displacement", "None"),
        "color": offer.get("color_hex", "None"),
        "url": offer.get("url", "None"),
    }


INCREMENT = 5000
with ThreadPoolExecutor(max_workers=30) as executor:
    future_to_price = {executor.submit(fetch_offers, price, price + INCREMENT): (price, price + INCREMENT) for price in range(1000, 10000001, INCREMENT)}

    for future in as_completed(future_to_price):
        price = future_to_price[future]
        try:
            future.result()
        except Exception as exc:
            print(f'Ошибка при парсинге с параметрами {price}: {exc}')
