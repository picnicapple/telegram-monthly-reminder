import os
import sys
import calendar
from datetime import datetime, timezone, timedelta
import urllib.request
import urllib.parse

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
MESSAGE = "이자납입일 확인 \n 이율 4.7%, 1억원*0.047/12=391,000원 \n 신한 110-188-653441"

KST = timezone(timedelta(hours=9))


def target_day_for_month(year: int, month: int) -> int:
    """해당 월의 마지막 날이 29일보다 작으면(2월 등) 그 마지막 날을,
    그렇지 않으면 29일을 반환한다."""
    last_day = calendar.monthrange(year, month)[1]
    return min(29, last_day)


def main() -> None:
    now = datetime.now(KST)
    expected_day = target_day_for_month(now.year, now.month)

    if now.day != expected_day:
        print(
            f"Today ({now.date()}) is not the target day "
            f"({expected_day} for {now.year}-{now.month:02d}). Skipping."
        )
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": CHAT_ID, "text": MESSAGE}).encode()
    req = urllib.request.Request(url, data=data)

    with urllib.request.urlopen(req) as resp:
        body = resp.read().decode()
        print(body)
        if resp.status != 200:
            sys.exit(1)


if __name__ == "__main__":
    main()
