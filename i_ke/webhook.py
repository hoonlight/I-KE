import logging
import httpx

logger = logging.getLogger(__name__)


def send_message(
    url: str, title: str, description: str, color: int, mention: bool = False
) -> str:
    try:
        params = {"wait": True}
        response = httpx.post(
            url,
            params=params,
            json={
                "content": "@everyone" if mention else "",
                "embeds": [
                    {"title": title, "description": description, "color": color}
                ],
            },
        )
        message_id = response.json().get("id")
        print(f"Message sent successfully with id: {message_id}")
    except httpx.HTTPError as e:
        print(e)

    return message_id


def edit_message(
    url: str,
    message_id,
    title: str,
    description: str,
    color: int,
) -> None:
    try:
        httpx.patch(
            url=f"{url}/messages/{message_id}",
            json={
                "embeds": [
                    {"title": title, "description": description, "color": color}
                ],
            },
        )
    except Exception as e:
        logger.exception(f"Failed to send discord webhook: {e}")

    logger.info("Message edited successfully")
