from datetime import timedelta
from functools import wraps

from carbonaware_prefect.delay import carbonaware_delay


def carbonaware_delay_decorator(
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

    Returns:
        A decorator function that can be applied to any function to delay its execution.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Apply the carbon-aware delay
            carbonaware_delay(
                window=window,
                duration=duration,
                region=region,
                provider=provider,
            )

            # Execute the wrapped function
            return func(*args, **kwargs)

        return wrapper

    return decorator
