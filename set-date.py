import re
import sys
from datetime import datetime

if len(sys.argv) != 2:
    print("Usage: python set-date.py <file_path>")
    sys.exit(1)

file_path = sys.argv[1]

def suffix(day):
    if 11 <= day <= 13:
        return 'th'
    return {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')

def format_date():
    now = datetime.now()
    return now.strftime(f"%B {now.day}{suffix(now.day)}, %Y")

def replace_date_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('$DATE$', format_date())
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

replace_date_in_file(file_path)
