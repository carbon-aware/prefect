import logging
import httpx
from carbonaware_scheduler.types.cloud_zone import CloudZone

AWS_METADATA_URL = "http://169.254.169.254/latest/meta-data"
AZURE_METADATA_URL = "http://169.254.169.254/metadata/instance/compute"

logger = logging.getLogger(__name__)


def detect_cloud_zone() -> CloudZone:
    # AWS example
    try:
        az = httpx.get(f"{AWS_METADATA_URL}/placement/availability-zone", timeout=0.5).text
        logger.debug(f"Detected AWS zone: {az}")
        region = az[:-1]
        return CloudZone(provider="aws", region=region)
    except Exception:
        pass

    # Azure example
    try:
        headers = {'Metadata': 'true'}
        response = httpx.get(
            f"{AZURE_METADATA_URL}/location?api-version=2021-02-01",
            headers=headers,
            timeout=0.5
        )
        region = response.text.strip().replace('"', '')
        logger.debug(f"Detected Azure region: {region}")
        return CloudZone(provider="azure", region=region)
    except Exception:
        pass

    # GCP example
    try:
        zone_path = httpx.get(
            "http://metadata.google.internal/computeMetadata/v1/instance/zone",
            headers={"Metadata-Flavor": "Google"},
            timeout=0.5,
        ).text
        region = zone_path.split("/")[-1][:-2]  # zones/us-central1-a → us-central1
        logger.debug(f"Detected GCP region: {region}")
        return CloudZone(provider="gcp", region=region)
    except Exception:
        pass

    raise RuntimeError("Could not detect cloud zone from metadata. Please specify explicitly.")
