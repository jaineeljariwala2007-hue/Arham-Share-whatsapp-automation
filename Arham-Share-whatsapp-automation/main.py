"""
Entry point - runs the polling loop continuously.
"""

import logging
import signal
import sys
import time

import config
import message_logger
import whatsapp_sender
from excel_monitor import ExcelMonitor

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/automation.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)

_running = True

def _handle_signal(sig, _frame):
    global _running
    logger.info("Shutdown signal received (%s). Stopping...", sig)
    _running = False

signal.signal(signal.SIGINT,  _handle_signal)
signal.signal(signal.SIGTERM, _handle_signal)


def main() -> None:
    logger.info("=== Arham Share - Inactive Client WhatsApp Automation started ===")

    if config.ENABLE_WEBHOOK:
        import webhook_server
        webhook_server.start_webhook_thread()

    already_messaged = message_logger.load_already_messaged()
    monitor = ExcelMonitor(already_messaged)
    logger.info("Loaded %d already-messaged phone(s) from log.", len(already_messaged))

    while _running:
        try:
            new_clients = monitor.poll()
            if new_clients:
                logger.info("Found %d new client(s) to message.", len(new_clients))
            for client in new_clients:
                name    = client[config.COL_CLIENT_NAME]
                phone   = client[config.COL_PHONE_NUMBER]
                success = whatsapp_sender.send_template_message(phone, name)
                message_logger.log_sent(name, phone, "Sent" if success else "Failed")
        except Exception as exc:
            logger.error("Unexpected error in polling loop: %s", exc, exc_info=True)

        for _ in range(config.POLL_INTERVAL_SECONDS):
            if not _running:
                break
            time.sleep(1)

    logger.info("=== Automation stopped cleanly. ===")


if __name__ == "__main__":
    main()