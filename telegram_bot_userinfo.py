import csv
import os
import shutil
import subprocess
import time
import traceback
from datetime import datetime
from functools import partial
from pathlib import Path

import pyautogui
import pyperclip
from PIL import ImageGrab

from liblogger import log_err, log_inf, log_warn

ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

CUR_DIR = str(Path(__file__).parent.absolute())
TDATA_LIST_DIR = os.path.join(CUR_DIR, "82tdata")
TELEGRAM_DIR = os.path.join(CUR_DIR, "Telegram")
TELEGRAM_BIN_PATH = os.path.join(TELEGRAM_DIR, "Telegram.exe")
TDATA_PATH = os.path.join(TELEGRAM_DIR, "tdata")

T_IMG_LOADING = "t_loading.png"
T_IMG_AUTH_ERROR = os.path.join(CUR_DIR, "t_auth_error.png")
T_IMG_TELEGRAM_CHANNEL = os.path.join(CUR_DIR, "t_telegram_channel.png")

T_IMG_USERINFOBOT_LINK = os.path.join(CUR_DIR, "t_userinfobot_link.png")
T_IMG_USERINFOBOT_WELCOME = os.path.join(CUR_DIR, "t_userinfobot_welcome.png")
T_IMG_USERINFOBOT_START = os.path.join(CUR_DIR, "t_userinfobot_start.png")
T_IMG_USERINFOBOT_ID = os.path.join(CUR_DIR, "t_userinfobot_id.png")
T_IMG_USERINFOBOT_COPY = os.path.join(CUR_DIR, "t_userinfobot_copy.png")

T_IMG_GROUP_JOIN_LINK = os.path.join(CUR_DIR, "t_group_join_link.png")
T_IMG_GROUP_JOIN_BTN = os.path.join(CUR_DIR, "t_group_join_btn.png")


def safe_rmtree(dir_path: str):
    while os.path.isdir(dir_path):
        try:
            shutil.rmtree(dir_path)
        except:
            # traceback.print_exc()
            # log_warn("retry")
            pass
        time.sleep(0.1)


def wait_for_img(img_path: str, timeout: float = 5):
    img_box = None
    start_tstamp = datetime.now().timestamp()
    while img_box == None:
        if datetime.now().timestamp() - start_tstamp > timeout:
            log_err("timeout")
            break
        try:
            img_box = pyautogui.locateOnScreen(img_path, confidence=0.9)
        except:
            pass
        time.sleep(0.1)
    time.sleep(0.5)
    return img_box


def wait_while_img(img_path: str, timeout: float = 30) -> bool:
    ret = True
    start_tstamp = datetime.now().timestamp()
    while True:
        if datetime.now().timestamp() - start_tstamp > timeout:
            log_err("timeout")
            ret = False
            break
        try:
            pyautogui.locateOnScreen(img_path, confidence=0.9)
        except:
            break
        time.sleep(0.1)
    time.sleep(0.5)
    return ret


def wait_and_click_img(img_path: str, timeout: float = 5):
    img_box = None
    start_tstamp = datetime.now().timestamp()
    while img_box == None:
        if datetime.now().timestamp() - start_tstamp > timeout:
            log_err("timeout")
            break
        try:
            img_box = pyautogui.locateOnScreen(img_path, confidence=0.9)
        except:
            pass
        time.sleep(0.1)
    if img_box != None:
        pyautogui.click(
            x=img_box.left + img_box.width // 2,
            y=img_box.top + img_box.height // 2,
        )
        time.sleep(0.5)


def wait_and_right_click_img(img_path: str, timeout: float = 5):
    img_box = None
    start_tstamp = datetime.now().timestamp()
    while img_box == None:
        if datetime.now().timestamp() - start_tstamp > timeout:
            log_err("timeout")
            break
        try:
            img_box = pyautogui.locateOnScreen(img_path, confidence=0.9)
        except:
            pass
        time.sleep(0.1)
    if img_box != None:
        pyautogui.rightClick(
            x=img_box.left + img_box.width // 2,
            y=img_box.top + img_box.height // 2,
        )
        time.sleep(0.1)


def work(tdata_dir_name: str):
    phone_number, username, telegram_id = "#", "#", "#"
    try:
        tdata_dir_path = os.path.join(TDATA_LIST_DIR, tdata_dir_name)
        phone_number = os.path.basename(tdata_dir_name)
        log_inf(f"phone: {phone_number}")
        src_tdata_dir_path = os.path.join(tdata_dir_path, "tdata")

        # copy tdata
        safe_rmtree(TDATA_PATH)
        shutil.copytree(src_tdata_dir_path, TDATA_PATH)

        # open telegram process
        log_inf("loading telegram ...")
        proc = subprocess.Popen([TELEGRAM_BIN_PATH])
        time.sleep(3)

        if wait_for_img(T_IMG_LOADING) != None:
            if wait_while_img(T_IMG_LOADING, 10):
                # check authentication
                if wait_for_img(T_IMG_AUTH_ERROR, timeout=1) == None:
                    # open telegram channel
                    pyautogui.hotkey("ctrl", "f", interval=0.01)
                    pyautogui.write("telegram", interval=0.01)
                    time.sleep(0.5)
                    wait_and_click_img(T_IMG_TELEGRAM_CHANNEL)

                    # join userinfobot channel
                    log_inf("join userinfobot channel ...")
                    pyautogui.write("tg://resolve?domain=userinfobot", interval=0.01)
                    pyautogui.press("enter")

                    wait_and_click_img(T_IMG_USERINFOBOT_LINK)

                    log_inf("loading ...")
                    wait_for_img(T_IMG_USERINFOBOT_WELCOME)
                    log_inf("start channel ...")
                    wait_and_click_img(T_IMG_USERINFOBOT_START, timeout=1)

                    # copy & write user information
                    wait_and_right_click_img(T_IMG_USERINFOBOT_ID)
                    wait_and_click_img(T_IMG_USERINFOBOT_COPY)
                    userinfo = pyperclip.paste()
                    lines = userinfo.split("\n")
                    username = lines[0].strip()
                    telegram_id = lines[1].replace("Id:", "").strip()
                    log_inf(f"     userinfo: {username}, {telegram_id}")
                else:
                    log_err("authentication error")
            else:
                log_err("loading timeout")
        else:
            log_err("loading image not found")
        # quit telegram
        proc.kill()
    except:
        traceback.print_exc()
    return phone_number, username, telegram_id


def main():
    try:
        userinfo_list = []

        tdata_dir_list = os.listdir(TDATA_LIST_DIR)
        for i, tdata_dir_name in enumerate(tdata_dir_list):
            print()
            log_inf(f"working on {i} / {len(tdata_dir_list)} ...")
            tdata_dir_path = os.path.join(TDATA_LIST_DIR, tdata_dir_name)
            if not os.path.isdir(tdata_dir_path):
                continue

            phone_number, username, telegram_id = work(tdata_dir_name=tdata_dir_name)
            userinfo_list.append(
                {
                    "phone": phone_number,
                    "username": username,
                    "telegram_id": telegram_id,
                }
            )

            with open(os.path.join(CUR_DIR, "telegram_users.csv"), "w") as f:
                writer = csv.writer(f)
                writer.writerow(["No", "Phone", "Username", "Id"])
                for i, userinfo in enumerate(userinfo_list):
                    writer.writerow([i, userinfo["phone"], userinfo["username"], userinfo["telegram_id"]])
    except:
        traceback.print_exc()


def test():
    work("+14504108476")
    work("+14504230543")


if __name__ == "__main__":
    main()
    # test()
    input("Press ENTER to exit.")
