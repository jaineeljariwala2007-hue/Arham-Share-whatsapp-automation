"""
Manages message_log.xlsx:
  Sheet "Messages Sent"  - one row per successfully messaged client
  Sheet "Client Replies" - first reply only per client
"""

import logging
import threading
from datetime import datetime
from pathlib import Path

import pandas as pd
from openpyxl import load_workbook

import config

logger = logging.getLogger(__name__)

_LOCK = threading.Lock()

SENT_COLS  = ["Client Name", "Phone Number", "Date & Time Sent", "Status"]
REPLY_COLS = ["Client Name", "Phone Number", "Reply Text", "Date & Time Received"]


def _ensure_log_file() -> None:
    path = Path(config.MESSAGE_LOG_FILE)
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        pd.DataFrame(columns=SENT_COLS).to_excel(writer, sheet_name="Messages Sent", index=False)
        pd.DataFrame(columns=REPLY_COLS).to_excel(writer, sheet_name="Client Replies", index=False)
    logger.info("Created %s", path)


def _append_row(sheet_name: str, row: dict) -> None:
    _ensure_log_file()
    path = Path(config.MESSAGE_LOG_FILE)
    with _LOCK:
        book = load_workbook(path)
        ws = book[sheet_name]
        ws.append(list(row.values()))
        book.save(path)


def load_already_messaged() -> set[str]:
    _ensure_log_file()
    try:
        df = pd.read_excel(config.MESSAGE_LOG_FILE, sheet_name="Messages Sent", dtype=str)
        sent = df[df["Status"].str.strip() == "Sent"]
        return set(sent["Phone Number"].dropna().str.strip().tolist())
    except Exception as exc:
        logger.error("Could not read messaged phones: %s", exc)
        return set()


def load_already_replied() -> set[str]:
    _ensure_log_file()
    try:
        df = pd.read_excel(config.MESSAGE_LOG_FILE, sheet_name="Client Replies", dtype=str)
        return set(df["Phone Number"].dropna().str.strip().tolist())
    except Exception as exc:
        logger.error("Could not read replied phones: %s", exc)
        return set()


def log_sent(client_name: str, phone: str, status: str = "Sent") -> None:
    _append_row("Messages Sent", {
        "Client Name":      client_name,
        "Phone Number":     phone,
        "Date & Time Sent": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Status":           status,
    })


def log_reply(client_name: str, phone: str, reply_text: str) -> None:
    _append_row("Client Replies", {
        "Client Name":          client_name,
        "Phone Number":         phone,
        "Reply Text":           reply_text,
        "Date & Time Received": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })
