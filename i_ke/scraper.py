import logging

import bs4
import httpx

url = "https://madeedam.com/goods/goods_view.php?goodsNo=1000001840"


logger = logging.getLogger(__name__)


def get_product_info(url: str) -> bs4.BeautifulSoup | None:
    logger.info("Getting product info...")
    try:
        response = httpx.get(url)
    except httpx.HTTPError as exc:
        print(f"An error occurred: {exc}")
        return None

    soup = bs4.BeautifulSoup(response.text, "html.parser")

    try:
        manual = soup.find("div", class_="txt-manual")
        manual = manual.get_text().strip()
    except Exception as e:
        print(e)

    try:
        stock_button = soup.find("div", class_="btn_choice_box btn_restock_box")
        stock_button = stock_button.get_text().strip()
    except Exception as e:
        print(e)

    return {"manual": manual, "stock_button": stock_button}
