import logging
import os

import requests

logger = logging.getLogger(__name__)

WAREHOUSE_API_URL = os.getenv(
    "WAREHOUSE_API_URL",
    "http://127.0.0.1:8001",
)

WAREHOUSE_USERNAME = os.getenv(
    "WAREHOUSE_USERNAME",
    "bookstore_service",
)

WAREHOUSE_PASSWORD = os.getenv(
    "WAREHOUSE_PASSWORD",
    "bookstore_service_password",
)


class WarehouseServiceError(Exception):
    pass


def get_access_token():
    url = f"{WAREHOUSE_API_URL}/api/token/"

    try:
        response = requests.post(
            url,
            json={
                "username": WAREHOUSE_USERNAME,
                "password": WAREHOUSE_PASSWORD,
            },
            timeout=5,
        )

        response.raise_for_status()

        return response.json()["access"]

    except (requests.RequestException, KeyError) as exc:
        logger.error("Could not get Warehouse JWT token: %s", exc)

        raise WarehouseServiceError(
            "Could not authenticate with Warehouse service."
        ) from exc


def reserve_stock(book_id, quantity):
    access_token = get_access_token()

    url = f"{WAREHOUSE_API_URL}/api/stock/{book_id}/reserve/"

    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    try:
        response = requests.post(
            url,
            json={"quantity": quantity},
            headers=headers,
            timeout=5,
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException as exc:
        logger.error(
            "Warehouse API error for book_id=%s: %s",
            book_id,
            exc,
        )

        raise WarehouseServiceError(
            "Could not reserve stock in Warehouse service."
        ) from exc
