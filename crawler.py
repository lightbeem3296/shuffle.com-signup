import os
import traceback
from pathlib import Path

from libchrome import Chrome
from liblogger import log_inf

CUR_DIR = str(Path(__file__).parent.absolute())
TEMP_DIR = os.path.join(CUR_DIR, "temp")
OUTPUT_DIR = os.path.join(CUR_DIR, "output")
USER_DATA_DIR = os.path.join(TEMP_DIR, "profile")

REGISTER_URL = "https://shuffle.com/?md-tab=register&modal=auth"


def register(chrome: Chrome, username: str, email: str, password: str):
    try:
        chrome.clear_cookie()

        chrome.goto(REGISTER_URL, wait_elem_selector="input[name='username']")

        chrome.set_value("input[name='username']", username)
        chrome.set_value("input[name='email']", email)
        chrome.set_value("input[name='password']", password)
        chrome.click("input[type='checkbox']")
        chrome.click("button[type='submit']")
    except:
        traceback.print_exc()


def main():
    try:
        CHROME = Chrome(
            width=800,
            height=600,
            block_image=True,
            user_data_dir=USER_DATA_DIR,
        )
        CHROME.start()

        CHROME.quit()
        log_inf("All done.")
    except:
        traceback.print_exc()


if __name__ == "__main__":
    main()
