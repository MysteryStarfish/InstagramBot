import os
from time import sleep
import random

from instagrapi import Client

import dotenv

dotenv.load_dotenv(".env")

USERNAME = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")

author_id = '65051551192'
auto_reply_ids = ['65206241525']

cl = Client()
cl.login(USERNAME, PASSWORD)
thread = cl.direct_threads(1)[0]
pre_message = thread.messages[0]

def get_latest_message(cl):
    thread = cl.direct_threads(1)[0]
    current_message = thread.messages[0]
    return current_message

def get_random_message():
    messages = ["確實", "真的欸", "有料", "要", "超好笑", "笑死", "嗯嗯", "喔不", "哇嘞"]
    message = random.choice(messages)
    return message

is_important_message = False
is_no_new_message = False

while True:
    current_message = get_latest_message(cl)
    if current_message.user_id == author_id:
        continue
    elif current_message.user_id not in auto_reply_ids:
        is_important_message = True
    elif current_message == pre_message:
        is_no_new_message = True
    
    if is_no_new_message:
        print("No new message")
        continue
    if is_important_message:
        print("Important Message!!!")
        continue

    is_important_message = False
    is_no_new_message = False

    pre_message = current_message
    print("New message")

    cl.direct_send(get_random_message(), user_ids = [current_message.user_id])
    
    sleep(1)