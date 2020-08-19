import schedule
import time


def job():
    print("I am working...")


def job_day():
    print("Do job day")


def start_job(func):
    # schedule.every().day.at("23:12").do(job_func=func)
    schedule.every(5).seconds.do(job_func=func)
    while True:
        # run_at_specific_time()
        schedule.run_pending()
        time.sleep(1)
