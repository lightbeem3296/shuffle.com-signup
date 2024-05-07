import os
import shutil
import subprocess
import time
import traceback
from datetime import datetime
from functools import partial
from pathlib import Path

import pyautogui
from PIL import ImageGrab

from liblogger import log_err, log_inf, log_warn

ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)


# TELEGRAM_GROUP_LINK = "https://t.me/+VpBfVmk9n_82ZjM0"
# TELEGRAM_GROUP_LINK = "https://t.me/+gM9UAN5ygO44ODU0"  # tg://join?invite=gM9UAN5ygO44ODU0
TELEGRAM_GROUP_LINK = None

CUR_DIR = str(Path(__file__).parent.absolute())
TDATA_LIST_DIR = os.path.join(CUR_DIR, "82tdata")
TELEGRAM_DIR = os.path.join(CUR_DIR, "Telegram")
TELEGRAM_BIN_PATH = os.path.join(TELEGRAM_DIR, "Telegram.exe")
TDATA_PATH = os.path.join(TELEGRAM_DIR, "tdata")

T_IMG_LOADING = os.path.join(CUR_DIR, "t_loading.png")
T_IMG_TELEGRAM_CHANNEL = os.path.join(CUR_DIR, "t_telegram_channel.png")
T_IMG_WRITE_A_MESSAGE = os.path.join(CUR_DIR, "t_write_a_message.png")

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
            img_box = pyautogui.locateOnScreen(img_path, confidence=0.9, grayscale=True)
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
            pyautogui.locateOnScreen(img_path, confidence=0.9, grayscale=True)
        except:
            break
        time.sleep(0.1)
    time.sleep(0.5)
    return ret


def wait_and_click_img(img_path: str, timeout: float = 5, region=None):
    img_box = None
    start_tstamp = datetime.now().timestamp()
    while img_box == None:
        if datetime.now().timestamp() - start_tstamp > timeout:
            log_err("timeout")
            break
        try:
            img_box = pyautogui.locateOnScreen(img_path, confidence=0.9, grayscale=True, region=region)
        except:
            pass
        time.sleep(0.1)
    if img_box != None:
        pyautogui.click(
            x=img_box.left + img_box.width // 2,
            y=img_box.top + img_box.height // 2,
        )
        time.sleep(0.1)
    time.sleep(0.5)


def wait_and_right_click_img(img_path: str, timeout: float = 5):
    img_box = None
    start_tstamp = datetime.now().timestamp()
    while img_box == None:
        if datetime.now().timestamp() - start_tstamp > timeout:
            log_err("timeout")
            break
        try:
            img_box = pyautogui.locateOnScreen(img_path, confidence=0.9, grayscale=True)
        except:
            pass
        time.sleep(0.1)
    if img_box != None:
        pyautogui.rightClick(
            x=img_box.left + img_box.width // 2,
            y=img_box.top + img_box.height // 2,
        )
        time.sleep(0.1)
    time.sleep(0.5)


def work(tdata_dir_name: str):
    try:
        tdata_dir_path = os.path.join(TDATA_LIST_DIR, tdata_dir_name)
        phone_number = os.path.basename(tdata_dir_name)
        log_inf(f"phone: {phone_number}")
        src_tdata_dir_path = os.path.join(tdata_dir_path, "tdata")

        # copy tdata
        safe_rmtree(TDATA_PATH)
        shutil.copytree(src_tdata_dir_path, TDATA_PATH)

        # open telegram process
        proc = subprocess.Popen([TELEGRAM_BIN_PATH])
        log_inf("loading telegram ...")
        time.sleep(3)

        if wait_for_img(T_IMG_LOADING) != None:
            if wait_while_img(T_IMG_LOADING, 10):
                # open telegram channel
                pyautogui.hotkey("ctrl", "f", interval=0.01)
                pyautogui.write("telegram", interval=0.01)
                time.sleep(0.5)
                wait_and_click_img(T_IMG_TELEGRAM_CHANNEL)

                # join group
                if TELEGRAM_GROUP_LINK != None:
                    group_id = TELEGRAM_GROUP_LINK.split("+", 1)[1].strip()
                    group_invite_link = f"tg://join?invite={group_id}"

                    pyautogui.write(group_invite_link, 0.01)
                    pyautogui.press("enter")

                    input_box = wait_for_img(T_IMG_WRITE_A_MESSAGE)
                    wait_and_click_img(T_IMG_GROUP_JOIN_LINK, region=(0, input_box.top-50, pyautogui.size().width, 100))
                    wait_and_click_img(T_IMG_GROUP_JOIN_BTN)
                    time.sleep(1)
            else:
                log_err("loading timeout")
        else:
            log_err("loading image not found")

        # quit telegram
        proc.kill()
    except:
        traceback.print_exc()


def main():
    try:
        tdata_dir_list = os.listdir(TDATA_LIST_DIR)
        for i, tdata_dir_name in enumerate(tdata_dir_list):
            log_inf(f"working on {i} / {len(tdata_dir_list)} ...")
            tdata_dir_path = os.path.join(TDATA_LIST_DIR, tdata_dir_name)
            if not os.path.isdir(tdata_dir_path):
                continue

            work(tdata_dir_name=tdata_dir_name)
    except:
        traceback.print_exc()


def test():
    work("+14504230538")


if __name__ == "__main__":
    main()
    # test()
    input("Press ENTER to exit.")
