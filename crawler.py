import os
import time
import traceback
from pathlib import Path

from libchrome import Chrome
from liblogger import log_inf

CUR_DIR = str(Path(__file__).parent.absolute())
TEMP_DIR = os.path.join(CUR_DIR, "temp")
OUTPUT_DIR = os.path.join(CUR_DIR, "output")
USER_DATA_DIR = os.path.join(TEMP_DIR, "profile")

REGISTER_URL = "https://shuffle.com/?md-tab=register&modal=auth"

ACCOUNT_LIST = [
    {
        "username": "testuser00",
        "email": "testuser00@email.com",
        "password": "123qwe!@#QWE",
    },
    {
        "username": "testuser01",
        "email": "testuser01@email.com",
        "password": "123qwe!@#QWE",
    },
    {
        "username": "testuser02",
        "email": "testuser02@email.com",
        "password": "123qwe!@#QWE",
    },
]


def register(chrome: Chrome, username: str, email: str, password: str):
    try:
        print()
        print()
        log_inf("*** register account ***")
        print()
        log_inf(f"username: {username}")
        log_inf(f"   email: {email}")
        log_inf(f"password: {password}")
        print()

        log_inf("clear old cookies ...")
        chrome.clear_cookie()

        log_inf("navigate to signup link ...")
        chrome.goto(REGISTER_URL, wait_elem_selector="input[name='username']")

        log_inf("fill signup form ...")
        chrome.set_value("input[name='username']", username)
        chrome.set_value("input[name='email']", email)
        chrome.set_value("input[name='password']", password)
        chrome.click("input[type='checkbox']")
        chrome.click("button[type='submit']")

        log_inf("waiting for puzzle ...")
        while chrome.url() != "https://shuffle.com/":
            time.sleep(0.1)
        log_inf("signup complete")
    except:
        traceback.print_exc()


def main():
    try:
        chrome = Chrome(
            width=800,
            height=800,
            user_data_dir=USER_DATA_DIR,
        )
        chrome.start()

        for account in ACCOUNT_LIST:
            register(
                chrome=chrome,
                username=account["username"],
                email=account["email"],
                password=account["password"],
            )

        input("Press ENTER to quit browser.")
        chrome.quit()
        log_inf("All done.")
    except:
        traceback.print_exc()


def test():
    chrome = Chrome(
        width=800,
        height=800,
        user_data_dir=USER_DATA_DIR,
    )
    chrome.start()

    register(
        chrome=chrome,
        username="testuser1",
        email="testuser1@email.com",
        password="124qwr!@$QWR",
    )

    input("Press ENTER to quit browser.")
    chrome.quit()


if __name__ == "__main__":
    main()
    # test()
    input("Press ENTER to exit.")
