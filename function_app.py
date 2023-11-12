import azure.functions as func
import logging

from blueprint import blueprint
from db import db_bp
from timer_function import timer_bp
from http3 import http3
from http3 import text_string

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

app.register_functions(blueprint)
app.register_functions(http3)
app.register_functions(db_bp)
app.register_functions(timer_bp)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
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
        text = text_string()
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed very successfully. {text}")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )