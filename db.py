# Register this blueprint by adding the following line of code 
# to your entry point file.  
# app.register_functions(db) 
# 
# Please refer to https://aka.ms/azure-functions-python-blueprints
import os

import azure.functions as func
import logging

from opencensus.ext.azure.log_exporter import AzureLogHandler

logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(connection_string=os.getenv('AI_CONNECTION_STRING')))
logger.setLevel(logging.INFO)

db_bp = func.Blueprint()

@db_bp.cosmos_db_trigger(arg_name = 'docs',
    database_name = os.getenv('database_id'),
    container_name = os.getenv('collection1_id'),
    connection = "cosmosdb_connection_str",
    lease_container_name='leases',
    create_lease_container_if_not_exists=True
)
def db(docs: func.DocumentList) -> str:
    logger.info('Python HTTP trigger function processed a request.')
    for doc in docs:
        logger.info(f"DB trigger data:{doc.data}")
    return None
