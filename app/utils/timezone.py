from datetime import datetime
from zoneinfo import ZoneInfo

from datetime import datetime, timedelta, timezone

NIGERIA_TZ = timezone(
    timedelta(hours=1)
)

def nigeria_now():

    return datetime.now(
        NIGERIA_TZ
    )