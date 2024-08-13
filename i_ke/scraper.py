import bs4
import httpx


def get_product_info(url: str) -> dict:
    try:
        response = httpx.get(url)
    except Exception as e:
        print(e)
        return {"manual": None, "stock_button": None}

    try:
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        manual = soup.find("div", class_="txt-manual")
        manual = manual.get_text().strip()
        stock_button = soup.find("div", class_="btn_choice_box btn_restock_box")
        stock_button = stock_button.get_text().strip()
    except Exception as e:
        print(e)
        return {"manual": None, "stock_button": None}

    return {"manual": manual, "stock_button": stock_button}
