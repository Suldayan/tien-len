import os
import sys
import shutil

def install_font(src):
    #correct font directory based on the OS
    if sys.platform == "win32":
        # Windows path: C:\Users\<User>\AppData\Local\Microsoft\Windows\Fonts
        dest_dir = os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Windows', 'Fonts')
    elif sys.platform == "darwin":
        # macOS path: ~/Library/Fonts
        dest_dir = os.path.expanduser("~/Library/Fonts")
    else:
        # Linux path: ~/.local/share/fonts
        dest_dir = os.path.expanduser("~/.local/share/fonts")
        
    #destination directory actually exists
    os.makedirs(dest_dir, exist_ok=True)
    
    # final destination path and copy the file
    font_name = os.path.basename(src)
    dest = os.path.join(dest_dir, font_name)
    
    shutil.copy(src, dest)