import os
from time import sleep
import random
import json
from instagrapi import Client
import dotenv

dotenv.load_dotenv(".env")

USERNAME = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")

with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

author_id = '65051551192'
auto_reply_ids = data['auto_reply_ids']

random_reply_messages = data['random_reply_messages']

cl = Client()
cl.login(USERNAME, PASSWORD)

thread = cl.direct_threads(1)[0]
pre_message = thread.messages[0]

def update():
    global pre_message
    
    current_message = get_latest_message(cl)
    if current_message == pre_message:
        return
    elif current_message.user_id == author_id:
        pass
    elif current_message.user_id not in auto_reply_ids:
        return

    if current_message.user_id == author_id:
        command(current_message)
        return

    main(current_message)

    print()

def command(current_message):
    if current_message.text.startswith("add_user"):
        user_name = add_user_to_auto_reply(current_message)

        send_message_to_author(f"已新增 {user_name} 至敷衍區")
        print(auto_reply_ids)
        print()

    elif current_message.text.startswith("remove_user"):
        user_name = remove_user_from_auto_reply(current_message)

        send_message_to_author(f"已移除 {user_name} 從敷衍區")
        print(auto_reply_ids)
        print()

    elif current_message.text.startswith("add_random"):
        reply_message = add_random_reply_message(current_message)

        send_message_to_author(f"已新增回覆: {reply_message}")
        print(random_reply_messages)
        print()

    elif current_message.text.startswith("remove_random"):
        reply_message = remove_random_reply_message(current_message)

        send_message_to_author(f"已移除回覆: {reply_message}")
        print(random_reply_messages)
        print()
        
    elif current_message.text.startswith("reply"):
        user_name, reply_message = process_reply_message(current_message)

        send_message_to_author(f"已傳送:\n{reply_message}\n給:\n{user_name}")
        print("Reply with: ", reply_message)
        print()

    elif current_message.text.startswith("global_reply"):
        reply_message = broadcast_reply_message(current_message)

        send_message_to_author(f"廣播訊息:\n{reply_message}\n給:{"、\n".join([cl.username_from_user_id(i) for i in auto_reply_ids])}")
        print("Reply with: ", reply_message, "to: ", [cl.username_from_user_id(i) for i in auto_reply_ids])
        
    elif current_message.text.startswith("stop"):
        pause_service(current_message)

def get_latest_message(cl):
    thread = cl.direct_threads(1)[0]
    current_message = thread.messages[0]
    return current_message

def add_user_to_auto_reply(current_message):
    user_name = current_message.text.split()[1]
    user_id = get_user_id_from_username(user_name)
    auto_reply_ids.append(user_id)
    save_data()
    return user_name

def remove_user_from_auto_reply(current_message):
    user_name = current_message.text.split()[1]
    user_id = get_user_id_from_username(user_name)
    auto_reply_ids.remove(user_id)
    save_data()
    return user_name

def get_user_id_from_username(user_name):
    user_id = cl.user_id_from_username(user_name)
    return user_id

def add_random_reply_message(current_message):
    reply_message = current_message.text.split(" ", 1)[1]
    random_reply_messages.append(reply_message)
    save_data()
    return reply_message

def remove_random_reply_message(current_message):
    reply_message = current_message.text.split(" ", 1)[1]
    random_reply_messages.remove(reply_message)
    save_data()
    return reply_message

def process_reply_message(current_message):
    user_name = current_message.text.split(" ", 2)[1]
    reply_message = current_message.text.split(" ", 2)[2]
    user_id = get_user_id_from_username(user_name)
    if "id" in reply_message: 
        reply_message = reply_message.split("id")[0]
        user_id = int(reply_message.split("id")[1])
    send_message_to_user(reply_message, user_id)
    return user_name,reply_message

def broadcast_reply_message(current_message):
    reply_message = current_message.text.split(" ", 1)[1]
    send_message_to_all_user(reply_message)
    return reply_message

def pause_service(current_message):
    try:
        delay_time = int(current_message.text.split(" ", 1)[1])
    except:
        delay_time = 30

    send_message_to_author(f"服務將暫停: {delay_time} 秒")
    print("Pause: ", delay_time)
    sleep(delay_time)
    send_message_to_author("服務已恢復")
    print("Resume")

def send_message_to_author(message):
    cl.direct_send(message, user_ids = [author_id])

def send_message_to_user(message, user_id):
    cl.direct_send(message, user_ids = [user_id])

def send_message_to_all_user(message):
    cl.direct_send(message, user_ids = auto_reply_ids)
    
def save_data():
    data['auto_reply_ids'] = auto_reply_ids
    data['random_reply_messages'] = random_reply_messages
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f)


def main(current_message):
    global pre_message

    pre_message = current_message
    print("New message: ", current_message.text)

    reply_message = get_auto_reply_message(current_message.text, current_message.user_id)
    if not reply_message: return
    send_message_to_user(reply_message, current_message.user_id)
    print("Reply with: ", reply_message)

def get_auto_reply_message(message, user_id):
    _msg = message
    ask = ["會", "可以", "要", "能", "應該", "該","好笑", "好", "是", "對", "有趣", "有", "真的", "知道", "可愛", "喜歡", "討厭"]
    _a = ["True" if i in _msg else "" for i in ask]
    no = random.randint(0, 1)
    no = "不" if no else ""
    end = random.choice(["", "啦", "~", "吧", "(X)", "耶", "欸", "咩"])

    func = ["+", "-", "*", "/", "(", ")"]
    _b = ["True" if i in _msg else "" for i in func]
    str_num = [str(i) for i in range(10)]

    if _msg == "你是誰":
        send_message_to_user("...", user_id)
        sleep(2)
        return "我...我才沒有被盜帳呢"
    elif _msg == "我是誰":
        send_message_to_user("...", user_id)
        sleep(2)
        return "問你啊"
    
    if any(_a):
        content = no + ask[_a.index("True")] + end
    elif "的" in _msg or "得" in _msg:
        keyWord = "得" if "得" in _msg else "的"
        content = _msg[_msg.index(keyWord) - 1] + random.choice([keyWord, "不"]) + _msg[_msg.index(keyWord) + 1] + end
    elif "嗎" in _msg:
        content = no + _msg[_msg.index("嗎") - 1] + end
    else:
        content = get_random_message()

    if any(_b):
        start = ""
        end = ""
        start_index = _msg.index(func[_b.index("True")])
        end_index = _msg.index(func[_b.index("True")])
        while start_index >= 0:
            if not (_msg[start_index] in func or _msg[start_index] in str_num):
                break
            start += _msg[start_index]
            start_index -= 1
        while end_index < len(_msg):
            if not (_msg[end_index] in func or _msg[end_index] in str_num):
                break
            end += _msg[end_index]
            end_index += 1
        content = start[::-1] + end[1:]
        content = str(eval(content))
    
    return content

def get_random_message():
    message = random.choice(random_reply_messages)
    return message

print("Link Start")
while True:
    update()
    sleep(0.5)