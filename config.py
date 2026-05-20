"""
Central configuration. Fill in all REQUIRED values before running.
"""

# -- WhatsApp Business API ---------------------------------------------------
WHATSAPP_API_URL = "https://graph.facebook.com/v25.0/{phone_number_id}/messages"
PHONE_NUMBER_ID  = "1021459374381952"
ACCESS_TOKEN     = "EAAfgWi8ZAFuIBRkm1Ikk0rn9ACTXtqgZBV1RhXhKpJZAqKZAAIwUcbdmJ7XwVJxLbZA2GzTZCOOhySK4iz02eqFdSUJBVj1t7pA1wO9skBqgmMGaHSsBISa1hTN2GLlG1gs8fsaqwzeGDulDyKCDKzdLbYX7KYnIe7Ko7QhZCl5HQ9MqlDAVBtzJzxudYusWk82TfHxDfxHfqArvBvk8Yd181fW6PmghZArDAe7JNmZBOWYXHzZAc1cBvTDkA02wQzibM3ToelYZBGZByeyYnKdqCZAV9LNAvrU8trR8HsQZDZD"

# Template details (must be approved in Meta Business Manager)
TEMPLATE_NAME     = "hello_world"
TEMPLATE_LANGUAGE = "en_US"

# -- File Paths ---------------------------------------------------------------
INACTIVE_CLIENTS_FILE = "C:/Users/Jaineel/Downloads/inactive_clients.xlsx"    # Excel file your team updates
MESSAGE_LOG_FILE      = "data/message_log.xlsx"    # auto-created by the script

# Column names in inactive_clients.xlsx (case-sensitive)
COL_CLIENT_NAME  = "Client Name"
COL_PHONE_NUMBER = "Phone Number"      # expected format: +91XXXXXXXXXX

# -- Polling ------------------------------------------------------------------
POLL_INTERVAL_SECONDS = 10    # check every 10 seconds

# -- Webhook (for receiving client replies) ------------------------------------
ENABLE_WEBHOOK       = True
WEBHOOK_HOST         = "0.0.0.0"
WEBHOOK_PORT         = 3000
WEBHOOK_VERIFY_TOKEN = "ek-thky-sedsk-578-as"
