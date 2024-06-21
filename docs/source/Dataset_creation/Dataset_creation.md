# Instructions for Creating a GCP Dataset for TQ42

## Initial Setup Requirements

1. **URI/URL Format**:
   - Format: `[storage_type]://[bucket_name]`.
   - Examples:
     - Google Cloud Storage: `gs://bucket_name`
     - AWS S3: `s3://aws_bucket` (currently not supported)
     - Azure Storage: `az://another_bucket` (currently not supported)

2. **GCP Service Account Name**:
   - Format: `project-[PROJECT_NUMBER]@storage-transfer-service.iam.gserviceaccount.com`.
   - Current Account: `project-988275624279@storage-transfer-service.iam.gserviceaccount.com`.
   - Note: This may change in the future. A single service account is shared across all customers.

## Sample Upload Workflow

1. **Create and Upload to Bucket**:
   - The user creates a bucket in their cloud environment and uploads the required files.

   ![Image 1: Bucket Creation and Upload Process](../images/dataset_image_1.png)

2. **Create a Custom Role**:
   - The user creates a new custom role using a provided template with the necessary permissions.

   ![Image 2: Custom Role Creation Template](../images/dataset_image_2.png)

3. **Edit Bucket Access**:
   - The user returns to their bucket to edit access settings.
   - Grant access to the service account: `project-988275624279@storage-transfer-service.iam.gserviceaccount.com`.
   - Assign the newly created role from step 2 to this service account.

   ![Image 3: Bucket Access Modification](../images/dataset_image_3.png)

4. **Run tq42 SDK for Storage and Data Transfer**:
   - The user runs the tq42 SDK to create new storage and transfer data.
   - Note: The URL format is `gs://[id_of_bucket]`.

```python
from tq42.client import TQ42Client
from tq42.dataset import Dataset, DatasetSensitivityProto

with TQ42Client() as client:
    dataset = Dataset.create(
        client=client,
        name="<NAME_OF_THE_NEW_DATASET>",
        description="<DESCRIPTION_OF_THE_NEW_DATASET>",
        url="gs://<THIS_IS_YOUR_BUCKET_URL>",
        sensitivity=DatasetSensitivityProto.SENSITIVE,
        project_id="<PROJECT_ID>",
    )
    print(dataset.id)
```

5. **Finalize Data Transfer**:
   - After the code execution, a new bucket with a random ID is created, and files are transferred into it.

   ![Image 5: Data Transfer Completion](../images/dataset_image_5.png)
