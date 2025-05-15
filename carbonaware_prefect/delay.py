import logging
import time
from datetime import datetime, timedelta, timezone
from functools import wraps

from carbonaware_scheduler import CarbonawareScheduler
from carbonaware_scheduler.types.cloud_zone import CloudZone
from carbonaware_scheduler.types.schedule_create_params import Window
import isodate

from carbonaware_prefect.introspection import detect_cloud_zone

logger = logging.getLogger(__name__)


def carbonaware_delay(
    window: timedelta = timedelta(hours=6),
    duration: timedelta = timedelta(minutes=30),
    region: str | None = None,
    provider: str | None = None,
):
    """Decorator to delay execution until a CO2-optimal time.

    If region and provider are not specified, and they can't be detected automatically,
    a warning will be logged and no delay will be applied.

    Args:
        window: The maximum delay to wait for an optimal time.
        duration: The duration of the job.
        region: The region of the cloud zone. If not specified, it will be detected automatically.
        provider: The provider of the cloud zone. If not specified, it will be detected automatically.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Determine location
            zone = CloudZone(provider=provider, region=region)
            if not provider or not region:
                try:
                    zone = detect_cloud_zone()
                except Exception:
                    logger.warning(
                        "Failed to detect cloud zone. Please specify provider and region explicitly. Running without delay."
                    )
                    return func(*args, **kwargs)

            client = CarbonawareScheduler()
            response = client.schedule.create(
                duration=isodate.duration_isoformat(duration),
                windows=[
                    Window(
                        start=datetime.now(tz=timezone.utc),
                        end=datetime.now(tz=timezone.utc) + window,
                    )
                ],
                zones=[zone],
            )

            ideal = response.ideal

            delay_seconds = (ideal.time - datetime.now(tz=timezone.utc)).total_seconds()
            if delay_seconds > 0:
                print(
                    f"[CarbonAware] Waiting {delay_seconds:.0f}s for optimal time: {ideal.time}"
                )
                time.sleep(delay_seconds)

            return func(*args, **kwargs)

        return wrapper

    return decorator
