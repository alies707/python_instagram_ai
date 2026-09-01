from apscheduler.schedulers.background import BackgroundScheduler


class SchedulerService:
    def __init__(self):
        self.scheduler = BackgroundScheduler()

    def add_job(self, func, interval_minutes=60):
        self.scheduler.add_job(func, 'interval', minutes=interval_minutes)

    def start(self):
        self.scheduler.start()
