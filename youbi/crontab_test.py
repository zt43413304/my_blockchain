import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()


def test():
    print("now is '%s' " % datetime.datetime.now())


scheduler.add_job(test, "cron", second="0, 30")

try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
