# Register this blueprint by adding the following line of code 
# to your entry point file.  
# app.register_functions(blueprint) 
# 
# Please refer to https://aka.ms/azure-functions-python-blueprints


import azure.functions as func
from azure.cosmos import CosmosClient
import logging
import os
import datetime
import uuid

from opencensus.ext.azure.log_exporter import AzureLogHandler

logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(connection_string=os.getenv('AI_CONNECTION_STRING')))
logger.setLevel(logging.INFO)

blueprint = func.Blueprint()


@blueprint.route(route="blueprint")
def http_trigger2(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        env = os.getenv('TEST1')

        id = uuid.uuid4().hex

        datetime_obj = datetime.datetime.now()
        datetime_str = datetime_obj.strftime('%Y%m%d_%H%M%S')
        data_to_log = {'id': id, 'name': name, 'datetime': datetime_str}

        cosmosdb_connection_str = os.environ["cosmosdb_connection_str"]
        client = CosmosClient.from_connection_string(cosmosdb_connection_str)
        database_id = os.environ["database_id"]
        database = client.get_database_client(database_id)
        collection_name = os.environ["collection1_id"]
        container_client = database.get_container_client(collection_name)
        logger.info(f"Adding data {data_to_log} to DB")
        new_log_item = container_client.create_item(body=data_to_log)

        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully. Env var {env}")
    else:
        # Return
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )