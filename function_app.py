import logging
import __run__ as r
import azure.functions as func

app = func.FunctionApp()

@app.schedule(schedule="0 */2 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def timer_trigger(myTimer: func.TimerRequest) -> None:
    
    logging.info('Python timer trigger function started.')

    try:
        ls = r.control()
    except Exception as e:
        logging.error(f'Could not run: {e}')

    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')