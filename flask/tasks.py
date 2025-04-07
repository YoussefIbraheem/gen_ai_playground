import time
from app import celery_app
from time import sleep
from progress.bar import Bar

@celery_app.task
def send_book_notification(book_id,title):
    print(f"Starting notification task for: {book_id}:{title}")
    with Bar('Processing...') as bar:
        for i in range(100):
            sleep(0.02)
            bar.next()
    print(f"Finished notification task for: {book_id}:{title}")

