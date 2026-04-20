# организация парсинга с сайта курсов валют

import requests

def get_exchange_rate(base_currency, target_currency):
    # получаем курс валют черех апи
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    try:
        response = requests.get(url)
        data = response.json()
        return data['rates'].get(target_currency)
    except Exception:
        return None