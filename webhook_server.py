"""
Optional Flask webhook server to receive incoming WhatsApp replies.
Only started when config.ENABLE_WEBHOOK = True.
"""

import logging
import threading

from flask import Flask, request, jsonify

import config
import message_logger

logger = logging.getLogger(__name__)

app = Flask(__name__)

_replied_phones: set[str] = set()
_replied_lock = threading.Lock()


def _init_replied_set() -> None:
    global _replied_phones
    _replied_phones = message_logger.load_already_replied()


@app.get("/webhook")
def verify():
    mode      = request.args.get("hub.mode")
    token     = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == config.WEBHOOK_VERIFY_TOKEN:
        logger.info("Webhook verified successfully.")
        return challenge, 200
    return "Forbidden", 403


@app.post("/webhook")
def receive():
    data = request.get_json(silent=True) or {}
    try:
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                _process_messages(change.get("value", {}))
    except Exception as exc:
        logger.error("Error processing webhook payload: %s", exc)
    return jsonify({"status": "ok"}), 200


def _process_messages(value: dict) -> None:
    messages = value.get("messages", [])
    contacts = value.get("contacts", [])

    name_map: dict[str, str] = {}
    for contact in contacts:
        wa_id = contact.get("wa_id", "")
        name  = contact.get("profile", {}).get("name", wa_id)
        if wa_id:
            name_map[wa_id] = name

    for msg in messages:
        if msg.get("type") != "text":
            continue

        phone         = msg.get("from", "")
        display_phone = f"+{phone}"
        reply_text    = msg.get("text", {}).get("body", "")
        client_name   = name_map.get(phone, display_phone)

        with _replied_lock:
            if display_phone in _replied_phones:
                logger.debug("Ignoring subsequent reply from %s", display_phone)
                continue
            _replied_phones.add(display_phone)

        message_logger.log_reply(client_name, display_phone, reply_text)
        logger.info("Recorded first reply from %s (%s)", client_name, display_phone)


def start_webhook_thread() -> None:
    _init_replied_set()
    t = threading.Thread(
        target=lambda: app.run(
            host=config.WEBHOOK_HOST,
            port=config.WEBHOOK_PORT,
            use_reloader=False,
        ),
        daemon=True,
        name="webhook-server",
    )
    t.start()
    logger.info("Webhook server listening on %s:%s", config.WEBHOOK_HOST, config.WEBHOOK_PORT)
