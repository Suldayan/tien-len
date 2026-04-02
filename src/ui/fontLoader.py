import shutil
import os

def install_font():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(base_dir, "..", "assets", "PixelifySans-Regular.ttf")
    dest = os.path.expanduser("~/Library/Fonts/PixelifySans-Regular.ttf")
    if not os.path.exists(dest):
        shutil.copy(src, dest)