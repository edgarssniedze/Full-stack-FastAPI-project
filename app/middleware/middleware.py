from fastapi import Request, BackgroundTasks
from datetime import datetime
from uuid import uuid7
import time

async def response_log(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    proc_time = time.perf_counter() - start_time

    log = {
        "request_id" : str(uuid7()),
        "time" : datetime.now(),
        "client" : request.client,
        "query": request.query_params,
        "method" : request.method,
        "path" : request.url.path,
        "process_time" : proc_time,
        "status_code" : response.status_code,
        "headers": response.headers,
    }

    response.background = BackgroundTasks()
    response.background.add_task(write_log, log)
    return response 

def write_log(data: dict):
    with open("log.txt", mode="a") as file:
        file.write(f"{str(data)} \n")
