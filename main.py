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

random_reply_messages = ["確實", "真的欸", "有料", "要", "超好笑", "笑死", "嗯嗯", "喔不", "哇嘞"]

cl = Client()
cl.login(USERNAME, PASSWORD)

thread = cl.direct_threads(1)[0]
pre_message = thread.messages[0]

def get_latest_message(cl):
    thread = cl.direct_threads(1)[0]
    current_message = thread.messages[0]
    return current_message

def get_random_message():
    message = random.choice(random_reply_messages)
    return message
    
def update():
    current_message = get_latest_message(cl)
    if current_message == pre_message:
        return
    elif current_message.user_id not in auto_reply_ids:
        return

    if current_message.user_id == author_id:
        if current_message.text.startswith("add"):
            user_name = current_message.text.split()[1]
            user_id = cl.user_id_from_username(user_name)
            auto_reply_ids.append(user_id)
            cl.direct_send(f"已新增 {user_name} 至敷衍區", user_ids = [author_id])
        elif current_message.text.startswith("remove"):
            user_name = current_message.text.split()[1]
            user_id = cl.user_id_from_username(user_name)
            auto_reply_ids.remove(user_id)
            cl.direct_send(f"已移除 {user_name} 從敷衍區", user_ids = [author_id])
        return

    pre_message = current_message
    print("New message: ", current_message.text)

    reply_message = get_random_message()
    cl.direct_send(reply_message, user_ids = [current_message.user_id])
    print("Reply with: ", reply_message)

    print()

while True:
    update()
    sleep(1)
    