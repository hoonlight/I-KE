import os
import time

import bs4
from playwright.sync_api import sync_playwright

from i_ke import webhook


def get_product_info(url: str) -> dict[str, str]:
    DISCORD_ADMIN_WEBHOOK_URL = os.getenv("DISCORD_ADMIN_WEBHOOK_URL")

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)

            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            )
            page = context.new_page()

            page.goto(url)

            time.sleep(5)

            content = page.content()
            browser.close()
        except Exception as e:
            print(e)
            return {"manual": None, "stock_button": None}

        try:
            soup = bs4.BeautifulSoup(content, "html.parser")
            manual = soup.find("div", class_="txt-manual")
            manual = manual.get_text(strip=True)
            stock_button = soup.find("div", class_="btn_choice_box btn_restock_box")
            stock_button = stock_button.get_text(strip=True)
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
