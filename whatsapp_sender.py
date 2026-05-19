"""
Sends WhatsApp template messages via the Meta Cloud API.
"""

import logging

import requests

import config

logger = logging.getLogger(__name__)

_SESSION = requests.Session()
_SESSION.headers.update({
    "Authorization": f"Bearer {config.ACCESS_TOKEN}",
    "Content-Type": "application/json",
})


def send_template_message(phone: str, client_name: str) -> bool:
    """
    Send the reactivation template to phone.
    Returns True on success, False on any error.
    """
    clean_phone = phone.lstrip("+")
    url = config.WHATSAPP_API_URL.format(phone_number_id=config.PHONE_NUMBER_ID)

    payload = {
        "messaging_product": "whatsapp",
        "to": clean_phone,
        "type": "template",
        "template": {
            "name": config.TEMPLATE_NAME,
            "language": {"code": config.TEMPLATE_LANGUAGE},
            # If your template has a variable like {{1}} for client name,
            # uncomment the block below:
            # "components": [
            #     {
            #         "type": "body",
            #         "parameters": [{"type": "text", "text": client_name}],
            #     }
            # ],
        },
    }

    try:
        resp = _SESSION.post(url, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        msg_id = data.get("messages", [{}])[0].get("id", "unknown")
        logger.info("Message sent to %s (%s), id=%s", client_name, phone, msg_id)
        return True
    except requests.exceptions.HTTPError as exc:
        logger.error(
            "HTTP error sending to %s (%s): %s - %s",
            client_name, phone, exc, exc.response.text if exc.response else "",
        )
    except requests.exceptions.RequestException as exc:
        logger.error("Network error sending to %s (%s): %s", client_name, phone, exc)

    return False
