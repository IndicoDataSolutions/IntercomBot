"""
Indico High Level Server Configurations
"""
import os

import indicoio
from intercom import Intercom

Intercom.app_id = os.getenv("INTERCOM_APP_ID")
Intercom.app_api_key = os.getenv("INTERCOM_API_KEY")
indicoio.config.api_key = os.getenv("INTERCOM_INDICO_API_KEY")

SECRET_MENTION_ID = '7ea04f5c9712c6ff7f7eb2f7afb5a9a6'
MENTION_TEMPLATE = """<a class="entity_mention %s" href="//app.intercom.io/apps/{intercom_app_id}/admin/{user_id}" rel="nofollow" target="_blank">{username}</a>"""
MENTION_TEMPLATE = MENTION_TEMPLATE % SECRET_MENTION_ID
ASSIGNMENT_THRESHOLD = 0.4
SUGGESTION_THRESHOLD = 0.1
COLLECTION_NAME = "triage-bot"
SUGGESTOR_ID = "USE_YOUR_OWN"
