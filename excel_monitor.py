"""
Watches inactive_clients.xlsx for newly added rows and yields them.
"""

import logging
from pathlib import Path

import pandas as pd

import config

logger = logging.getLogger(__name__)


def _read_clients(path: str) -> pd.DataFrame:
    try:
        df = pd.read_excel(path, dtype=str)
        df.columns = df.columns.str.strip()
        df = df.dropna(subset=[config.COL_CLIENT_NAME, config.COL_PHONE_NUMBER])
        df[config.COL_PHONE_NUMBER] = df[config.COL_PHONE_NUMBER].str.strip()
        return df.reset_index(drop=True)
    except FileNotFoundError:
        logger.warning("Inactive clients file not found: %s", path)
        return pd.DataFrame()
    except Exception as exc:
        logger.error("Could not read %s: %s", path, exc)
        return pd.DataFrame()


class ExcelMonitor:
    """Polls the Excel file and emits rows that have never been seen before."""

    def __init__(self, already_messaged: set[str]):
        self._seen_phones: set[str] = set(already_messaged)

    def poll(self) -> list[dict]:
        df = _read_clients(config.INACTIVE_CLIENTS_FILE)
        if df.empty:
            return []

        new_clients = []
        for _, row in df.iterrows():
            phone = row[config.COL_PHONE_NUMBER]
            if phone not in self._seen_phones:
                self._seen_phones.add(phone)
                new_clients.append(row.to_dict())

        return new_clients
