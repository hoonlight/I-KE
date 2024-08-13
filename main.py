import os
import time
from datetime import datetime
import logging

import dotenv

from i_ke import scraper
from i_ke import webhook


logger = logging.getLogger(__name__)

dotenv.load_dotenv()


def main():
    DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
    IKE_URL = os.getenv("IKE_URL")
    MESSAGE_ID = os.getenv("MESSAGE_ID")

    while True:
        if not MESSAGE_ID:
            webhook.send_message(DISCORD_WEBHOOK_URL, "starting...")
            break

        result = scraper.get_product_info(IKE_URL)

        manual = result.get("manual")
        stock_button = result.get("stock_button")

        if not stock_button == "구매 불가":
            webhook.send_message(
                DISCORD_WEBHOOK_URL, MESSAGE_ID, "상품 메시지 업데이트!"
            )
            break

        if not manual.startswith("** 2/29(목) 12:00"):
            webhook.edit_message(
                DISCORD_WEBHOOK_URL, MESSAGE_ID, "입고일 공지 업데이트!"
            )

        # 최종 업데이트 시간: format으로 현재 시간으로 보내기
        update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        title = "I-KE 알리미"
        info = "❗ 입고일 공지가 변경되거나, 상품이 입고되면 전체 알림을 보내드려요.\n\n🌐 [직접 확인하러 가기 <<< click](https://madeedam.com/goods/goods_view.php?goodsNo=1000001840)"

        description = f"*\n**✅ 실시간 감지 - {update_time} updated\n\n\n🚫 현재 상태: {stock_button}\n\n 📅 최근 공지: {manual[2:16]}\n\n\n{info}**"
        webhook.edit_message(
            DISCORD_WEBHOOK_URL, MESSAGE_ID, title, description, 0xFF0000
        )

        logger.info("Waiting for the next update...")
        time.sleep(60)

        return False

    return True


if __name__ == "__main__":
    main()
