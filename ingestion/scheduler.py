from apscheduler.schedulers.blocking import BlockingScheduler
from main import ingest_images

sched = BlockingScheduler()

@sched.scheduled_job("interval", seconds=30)
def job():
    ingest_images()

if __name__ == "__main__":
    sched.start()