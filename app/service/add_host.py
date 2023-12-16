import platform
import os

def add_entry_to_hosts_file(domain, ip):
    try:
        # تشخیص سیستم عامل
        system_platform = platform.system()

        # تعیین مسیر فایل hosts بر اساس سیستم عامل
        if system_platform == 'Windows':
            hosts_path = r'C:\Windows\System32\drivers\etc\hosts'
        elif system_platform == 'Linux' or system_platform == 'Darwin':
            hosts_path = '/etc/hosts'
        else:
            return

        # اضافه کردن نگاشت به فایل hosts
        with open(hosts_path, 'a') as hosts_file:
            hosts_file.write(f'{ip}\t{domain}\n')

    except Exception as e:
        pass
