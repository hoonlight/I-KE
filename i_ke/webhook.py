import logging
import httpx

logger = logging.getLogger(__name__)


def send_message(url: str, message: str):
    try:
        httpx.post(url, json={"content": message})
    except httpx.HTTPError as e:
        print(e)


def edit_message(
    url: str, message_id, title: str, description: str, color: int
) -> None:
    try:
        httpx.patch(
            url=f"{url}/messages/{message_id}",
            json={
                "content": "",
                "embeds": [
                    {"title": title, "description": description, "color": color}
                ],
            },
        )
    except Exception as e:
        logger.exception(f"Failed to send discord webhook: {e}")

    logger.info("Message edited successfully")
