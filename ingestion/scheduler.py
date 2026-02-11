from apscheduler.schedulers.blocking import BlockingScheduler
from main import ingest_once

sched = BlockingScheduler()

@sched.scheduled_job("interval", minutes=5)
def job():
    ingest_once()

if __name__ == "__main__":
    sched.start()