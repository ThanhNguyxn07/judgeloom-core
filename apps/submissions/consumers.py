from __future__ import annotations

from typing import Any

from channels.generic.websocket import AsyncJsonWebSocketConsumer


class SubmissionConsumer(AsyncJsonWebSocketConsumer):
    """Streams real-time submission updates to clients via WebSocket."""

    group_name: str

    async def connect(self) -> None:
        """Accept connection and subscribe client to the submission group."""
        submission_id = self.scope["url_route"]["kwargs"]["submission_id"]
        self.group_name = f"submission_{submission_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code: int) -> None:
        """Remove client from the submission group.

        Args:
            close_code: WebSocket close status code.
        """
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content: dict[str, Any], **kwargs: Any) -> None:
        """Handle incoming messages from clients.

        Args:
            content: Incoming JSON payload.
            **kwargs: Additional channel kwargs.
        """
        if content.get("type") == "ping":
            await self.send_json({"type": "pong"})

    async def broadcast(self, event: dict[str, Any]) -> None:
        """Forward channel-layer events to the WebSocket client.

        Args:
            event: Channel event payload containing update data.
        """
        payload = event.get("payload", {})
        await self.send_json(payload)
