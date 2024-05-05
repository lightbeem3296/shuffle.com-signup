import os
import shutil
import time
import traceback
from pathlib import Path

from liblogger import log_inf

CUR_DIR = str(Path(__file__).parent.absolute())
TDATA_LIST_DIR = os.path.join(CUR_DIR, "82tdata")
TELEGRAM_DIR = os.path.join(CUR_DIR, "Telegram")
TELEGRAM_BIN_PATH = os.path.join(TELEGRAM_DIR, "Telegram.exe")
TDATA_PATH = os.path.join(TELEGRAM_DIR, "tdata")


def safe_rmtree(dir_path: str):
    while os.path.isdir(dir_path):
        try:
            shutil.rmtree(dir_path)
        except:
            traceback.print_exc()
        time.sleep(0.1)


def main():
    try:
        tdata_dir_list = os.listdir(TDATA_LIST_DIR)
        for tdata_dir_name in tdata_dir_list:
            tdata_dir_path = os.path.join(TDATA_LIST_DIR, tdata_dir_name)
            if not os.path.isdir(tdata_dir_path):
                continue

            phone_number = tdata_dir_name
            log_inf(f"phone: {phone_number}")
            src_tdata_dir_path = os.path.join(tdata_dir_path, "tdata")

            safe_rmtree(TDATA_PATH)
            shutil.copytree(src_tdata_dir_path, TDATA_PATH)

            
    except:
        traceback.print_exc()


if __name__ == "__main__":
    main()
    input("Press ENTER to exit.")
