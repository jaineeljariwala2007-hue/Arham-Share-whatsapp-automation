"""
Central configuration. Fill in all REQUIRED values before running.
"""

# -- WhatsApp Business API ---------------------------------------------------
WHATSAPP_API_URL = "https://graph.facebook.com/v19.0/{phone_number_id}/messages"
PHONE_NUMBER_ID  = "YOUR_PHONE_NUMBER_ID"          # REQUIRED
ACCESS_TOKEN     = "YOUR_WHATSAPP_ACCESS_TOKEN"     # REQUIRED

# Template details (must be approved in Meta Business Manager)
TEMPLATE_NAME     = "reactivate_account"            # REQUIRED - your template name
TEMPLATE_LANGUAGE = "en"                            # change if template is in another language

# -- File Paths ---------------------------------------------------------------
INACTIVE_CLIENTS_FILE = "data/inactive_clients.xlsx"   # Excel file your team updates
MESSAGE_LOG_FILE      = "data/message_log.xlsx"         # auto-created by the script

# Column names in inactive_clients.xlsx (case-sensitive)
COL_CLIENT_NAME  = "Client Name"
COL_PHONE_NUMBER = "Phone Number"      # expected format: +91XXXXXXXXXX

# -- Polling ------------------------------------------------------------------
POLL_INTERVAL_SECONDS = 300    # how often to check the Excel file (every 5 minutes)

# -- Webhook (for receiving client replies) ------------------------------------
# Set ENABLE_WEBHOOK = True only if you have a public URL for your server.
# When False the script runs in send-only mode and "Client Replies" sheet
# stays empty until you enable the webhook.
ENABLE_WEBHOOK       = False
WEBHOOK_HOST         = "0.0.0.0"
WEBHOOK_PORT         = 5000
WEBHOOK_VERIFY_TOKEN = "YOUR_WEBHOOK_VERIFY_TOKEN"  # any secret string you choose
