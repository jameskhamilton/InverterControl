import logging
import __run__ as r
import asyncio
import azure.functions as func

app = func.FunctionApp()

@app.schedule(schedule="0 5 * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def timer_trigger(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    asyncio.run(r.control())

    logging.info('Python timer trigger function executed.')