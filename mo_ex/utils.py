import requests
from django.db import transaction
from decouple import config
from mo_ex.models import Security, History

SECURITIES_URL = config('SECURITIES_URL')
HISTORY_URL = config('HISTORY_URL')


def fetch_data(url):
    """Загружает данные из указанного URL."""
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def load_data():
    """Загружает данные в таблицы Security и History."""
    securities_data = fetch_data(SECURITIES_URL)
    history_data = fetch_data(HISTORY_URL)

    securities_records = securities_data[1]['securities'][1]
    history_records = history_data[1]['history'][1]

    with transaction.atomic():
        for record in securities_records:
            Security.objects.update_or_create(
                id=record['id'],
                secid=record['secid'],
                name=record['name'],
                defaults={
                    'regnumber': record.get('regnumber'),
                    'emitent_title': record.get('emitent_title'),
                }
            )

        for record in history_records:
            security = Security.objects.filter(secid=record['SECID']).first()
            if not security:
                continue

            History.objects.update_or_create(
                secid=security,
                tradedate=record['TRADEDATE'],
                defaults={
                    'numtrades': record.get('NUMTRADES', 0),
                    'open': record.get('OPEN'),
                    'close': record.get('CLOSE'),
                }
            )


if __name__ == "__main__":
    load_data()
