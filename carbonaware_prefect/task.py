from datetime import timedelta
from prefect import task

from carbonaware_prefect.delay import carbonaware_delay


def carbonaware_delay_task(
    window: timedelta = timedelta(hours=6),
    duration: timedelta = timedelta(minutes=30),
    region: str | None = None,
    provider: str | None = None,
    **task_kwargs,
):
    """
    Creates a Prefect task that delays execution until a CO2-optimal time.

    If region and provider are not specified, and they can't be detected automatically,
    a warning will be logged and no delay will be applied.

    Args:
        window: The maximum delay to wait for an optimal time.
        duration: The duration of the job.
        region: The region of the cloud zone. If not specified, it will be detected automatically.
        provider: The provider of the cloud zone. If not specified, it will be detected automatically.
        **task_kwargs: Additional keyword arguments to pass to the Prefect task.

    Returns:
        A Prefect task that delays execution until a CO2-optimal time.
    """

    # Create a task that performs the carbon-aware delay
    @task(**task_kwargs)
    def _carbonaware_delay_task():
        carbonaware_delay(
            window=window,
            duration=duration,
            region=region,
            provider=provider,
        )

    return _carbonaware_delay_task
