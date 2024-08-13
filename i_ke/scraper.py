import os

import bs4
import httpx

from i_ke import webhook


def get_product_info(url: str) -> dict[str, str]:
    DISCORD_ADMIN_WEBHOOK_URL = os.getenv("DISCORD_ADMIN_WEBHOOK_URL")

    try:
        response = httpx.get(url)
    except Exception as e:
        print(e)
        if DISCORD_ADMIN_WEBHOOK_URL:
            webhook.send_message(
                DISCORD_ADMIN_WEBHOOK_URL,
                title="Error",
                description=str(e),
                color=0xFF0000,
                mention=True,
            )
        return {"manual": None, "stock_button": None}

    try:
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        manual = soup.find("div", class_="txt-manual")
        manual = manual.get_text().strip()
        stock_button = soup.find("div", class_="btn_choice_box btn_restock_box")
        stock_button = stock_button.get_text().strip()
    except Exception as e:
        print(e)
        if DISCORD_ADMIN_WEBHOOK_URL:
            webhook.send_message(
                DISCORD_ADMIN_WEBHOOK_URL,
                title="Error",
                description=str(e),
                color=0xFF0000,
                mention=True,
            )
        return {"manual": None, "stock_button": None}

    return {"manual": manual, "stock_button": stock_button}
