from datetime import timedelta
from prefect import flow, task
from carbonaware_prefect import carbonaware_delay_task


@task
def train_model():
    print("✅ Training started at carbon-optimal time!")
    # Simulated training workload
    import time

    time.sleep(10)
    print("🏁 Training completed!")


@flow
def training_pipeline():
    print("🚀 Launching carbon-aware training pipeline...")

    # Create a carbon-aware delay task with specific parameters
    delay = carbonaware_delay_task(
        provider="gcp",  # Optional, if workload is running in the cloud (azure, aws, or gcp)
        region="us-central1",  # Optional, if workload is running in the cloud
        window=timedelta(
            minutes=5
        ),  # Max time to wait for a better time (e.g. 5 minutes)
        duration=timedelta(minutes=30),  # Estimated duration of the job
    )

    # Execute the delay task first
    delay()

    # Then run the actual training task
    train_model()


if __name__ == "__main__":
    training_pipeline()
