import pandas as pd
from azure.storage.blob import BlobServiceClient

def extract():
    df = pd.read_csv('/home/azureuser/airflow/data/raw/Superstore.csv')

    blob_service_client = BlobServiceClient.from_connection_string("<connection string>")
    blob_client = blob_service_client.get_blob_client(container="retail", blob="raw/superstore.csv")

    with open("/home/azureuser/airflow/data/raw/Superstore.csv", "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
