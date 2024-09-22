import logging
from typing import Any

from slack_sdk import WebClient

from app.models.integrations.slack import (
    SlackGetChannelIdRequest,
    SlackSendMessageRequest,
)

logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)


class SlackClient:
    def __init__(self, access_token: str):
        self.client = WebClient(token=access_token)

    def get_all_channel_ids(
        self, request: SlackGetChannelIdRequest
    ) -> list[dict[str, Any]]:
        response = self.client.conversations_list()
        channels = response["channels"]
        request_channel_names_set: set[str] = {
            name.lower() for name in request.channel_names
        }
        channel_info = [
            {"channel_name": channel["name"], "channel_id": channel["id"]}
            for channel in channels
            if channel["name"].lower()
            in request_channel_names_set  # Slack channel names are always lower case
        ]
        return channel_info

    def send_message(self, request: SlackSendMessageRequest):
        response = self.client.chat_postMessage(
            channel=request.channel_id, text=request.text
        )
        return response
