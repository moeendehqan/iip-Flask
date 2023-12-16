
from app import create_app
import asyncio
from app.service.add_host import add_entry_to_hosts_file
import socket

import threading
from app.service.CameraHandle import CameraHandle
from app.models.Connection import Connection

app = create_app()

connection_models = Connection()
connection_list = connection_models.get_all_id_connection()
amerahandle_models = CameraHandle()


if __name__ == "__main__":
    add_entry_to_hosts_file('vsc.server','127.0.0.2')

    local_ip = socket.gethostbyname('vsc.server')
    # ایجاد تعدادی ترد جداگانه برای اجرای توابع تکراری
    threads = []
    for i in connection_list:
        thread = threading.Thread(target=amerahandle_models.record, args=(i,))
        threads.append(thread)
        thread.start()

    app.run(host=local_ip, port=8080, debug=True)
#serve(app, host='0.0.0.0', port=8080)
