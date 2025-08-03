import pandas as pd
from azure.storage.blob import BlobServiceClient

def transform():
    # Load raw file
    df = pd.read_csv('/home/azureuser/airflow/data/raw/Superstore.csv', encoding='ISO-8859-1')

    # Clean + transform
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Total'] = df['Sales'] * df['Quantity']

    # Save to processed folder
    df.to_csv('/home/azureuser/airflow/data/processed/clean_superstore.csv', index=False)

    # Upload to Azure Blob
    blob_service_client = BlobServiceClient.from_connection_string("<Connect string>")
    blob_client = blob_service_client.get_blob_client(container="retail", blob="processed/clean_superstore.csv")

    with open('/home/azureuser/airflow/data/processed/clean_superstore.csv', 'rb') as f:
        blob_client.upload_blob(f, overwrite=True)

if __name__ == "__main__":
    transform()
