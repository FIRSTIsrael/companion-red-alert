import os
import logging
from datetime import datetime, timedelta, timezone
from requests import request, HTTPError, JSONDecodeError
from time import sleep
from config import ALERT_URL, POLLING_FREQUENCY_SECONDS

logger = logging.getLogger(__name__)
last_notification_time = None
notification_threshold = timedelta(minutes=1, seconds=30)
should_send_test_notification = os.getenv("TEST_MODE", False).lower() == "true"

companion_hostname = os.getenv("COMPANION_HOSTNAME", "http://127.0.0.1:8000")
companion_hostname = companion_hostname.replace("127.0.0.1", "host.docker.internal")
companion_hostname = companion_hostname.replace("localhost", "host.docker.internal")

page, row, column = os.getenv("COMPANION_BUTTON_LOCATION", "1,3,7").split(",")
red_alert_zones = os.getenv("RED_ALERT_ZONES")
if red_alert_zones is not None:
    red_alert_zones = red_alert_zones.split(",")
else:
    red_alert_zones = []
logger.info(f"Listening on: {red_alert_zones}")


def fetch_alerts():
    alerts = {}
    try:
        response = request("GET", ALERT_URL, headers={"Accept": "application/json"})
        response.raise_for_status()
        if len(alerts) == 0:
            return alerts
        alerts = response.json()
        logger.debug(f"Curernt red alerts: {alerts}")
    except HTTPError as error:
        logger.error(f"HTTP Error occured: {error}")
    except JSONDecodeError as error:
        logger.error(f"Received invalid alerts JSON: {error}")
    finally:
        return alerts


def should_notify(alerts):
    zones = alerts.get("data", [])
    is_relevant = False
    for zone in zones:
        if zone in red_alert_zones:
            is_relevant = True

    already_alerted = (
        last_notification_time is not None
        and datetime.now(timezone.utc) - last_notification_time > notification_threshold
    )

    if is_relevant and not already_alerted:
        return True
    return False


def notify():
    logger.info(f"Sending red alert notification to {companion_hostname}")
    global last_notification_time
    last_notification_time = datetime.now(timezone.utc)
    url = f"{companion_hostname}/api/location/{page}/{row}/{column}/press"
    request("POST", url)


if should_send_test_notification:
    logger.info("Sending test notification.")
    notify()

logger.info("Starting up")
while True:
    alerts = fetch_alerts()
    if should_notify(alerts):
        notify()
    sleep(POLLING_FREQUENCY_SECONDS)
