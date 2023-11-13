# Register this blueprint by adding the following line of code 
# to your entry point file.  
# app.register_functions(timer) 
# 
# Please refer to https://aka.ms/azure-functions-python-blueprints

import azure.functions as func
import datetime
import logging

from opencensus.ext.azure.log_exporter import AzureLogHandler

logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(connection_string=os.getenv('AI_CONNECTION_STRING')))
logger.setLevel(logging.INFO)
timer_bp = func.Blueprint()


@timer_bp.timer_trigger(schedule="0 0 * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def timer_trigger(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    datetime_obj = datetime.datetime.now()
    datetime_str = datetime_obj.strftime('%Y%m%d_%H%M%S')

    logger.info(f"Python timer trigger function executed at time {datetime_str}.")