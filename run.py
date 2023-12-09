
from app import create_app
import asyncio
import time

import threading

def repeat_task(task_id):
    while True:
        # کد تکراری که می‌خواهید اجرا شود
        print(f"Task {task_id} is repeated!")
        time.sleep(3)  # تعیین زمان تاخیر بین هر اجرا
        

app = create_app()


if __name__ == "__main__":
    num_tasks = 3

    # ایجاد تعدادی ترد جداگانه برای اجرای توابع تکراری
    threads = []
    for i in range(num_tasks):
        thread = threading.Thread(target=repeat_task, args=(i,))
        threads.append(thread)
        thread.start()

    app.run(host='0.0.0.0', port=8080, debug=True)
#serve(app, host='0.0.0.0', port=8080)
