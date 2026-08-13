import time
from datetime import datetime

def add_user_log(username):
    time.sleep(3)
    with open('user-log.txt', 'a') as file:
        file.write(f"{datetime.now()} | User {username} created\n")
    print("Користувача додано")


def add_post_log(title: str, username: str):
    time.sleep(3)
    with open('posts-log.txt', 'a') as file:
        file.write(f"{datetime.now()} |"
                   f" Post {title} created by {username}\n")
    print("Пост створено")

def change_post_log(id: int, username: str):
    time.sleep(3)
    with open("posts-log.txt", 'a') as file:
        file.write(f"{datetime.now()} | "
                    f"Post {id} changed by {username}\n")

def delete_post_log(id: int, username: str):
    time.sleep(3)
    with open("posts-log.txt", 'a') as file:
        file.write(f"{datetime.now()} | "
                   f"Post {id} deleted by {username}\n")

