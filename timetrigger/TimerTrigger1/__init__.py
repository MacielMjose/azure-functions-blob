import datetime
import logging

import os
import azure.functions as func
from azure.storage.blob import BlobServiceClient, ContainerClient


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    logging.info('Funcao bakup executada as: %s', utc_timestamp)
    copy_azure_files()

def copy_azure_files():
    # env_storage = os.environ["AzureWebJobsStorage"]
    env_storage = "DefaultEndpointsProtocol=https;AccountName=azfuncsanonymous;AccountKey=fBIJHusQHOp5I1Wq072On7M/D4/+Wk2bF0jsKa/nF3PdANDr8jF91k9jQKspvnLav4dGdVfbdGJU+AStjL4o4w==;EndpointSuffix=core.windows.net"
    logging.info(f'o ambiente lido e {env_storage}')
    blob_service = BlobServiceClient.from_connection_string(env_storage)
    
    container_client_prod = blob_service.get_container_client('prod')
    container_client_bkp = blob_service.get_container_client('bkp')

    
    logging.info("\nList blobs in the container")
    listagem = container_client_prod.list_blobs()
    if not listagem:
        logging.info("Sem dados para transferir do container prod para bkp.")
    else:
        for blob in listagem:
            source_blob_client = container_client_prod.get_blob_client(blob.name)
            destination_blob_client = container_client_bkp.get_blob_client(blob.name)
            destination_blob_client.start_copy_from_url(source_blob_client.url)
            logging.info(blob.name)