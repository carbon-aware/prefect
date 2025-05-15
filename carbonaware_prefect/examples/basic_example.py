from datetime import timedelta
from prefect import flow, task
from carbonaware_prefect.delay import carbonaware_delay

# This task will delay execution until a CO2-optimal window is available
@task
@carbonaware_delay(
    provider="gcp",        # Optional, if workload is running in the cloud (azure, aws, or gcp)
    region="us-central1",  # Optional, if workload is running in the cloud
    window=timedelta(minutes=5),  # Max time to wait for a better time (e.g. 10 minutes)
    duration=timedelta(minutes=30),  # Estimated duration of the job
)
def train_model():
    print("✅ Training started at carbon-optimal time!")
    # Simulated training workload
    import time
    time.sleep(10)
    print("🏁 Training completed!")

@flow
def training_pipeline():
    print("🚀 Launching carbon-aware training pipeline...")
    train_model()

if __name__ == "__main__":
    training_pipeline()
