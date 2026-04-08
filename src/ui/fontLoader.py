import os
import sys
import shutil
import subprocess

SUPPORTED_EXTENSIONS = {".ttf", ".otf", ".woff", ".woff2"}

def install_font(src):
    #correct font directory based on the OS

    """
    Install a font file to the appropriate system directory.

    Argument:
        src: Path to the font file to install.

    Returns:
        True if installation succeeded, False otherwise.
    """
    # validate src file
    if not os.path.isfile(src):
        print(f"Error: Font file not found: {src}")
        return False
    
    ext = os.path.splitext(src)[1].lower()
    if ext not in SUPPORTED_EXTENSIONS:
        print(f"Error: Unsupported font format '{ext}'. Expected one of {SUPPORTED_EXTENSIONS}")
        return False

    if sys.platform == "win32":
        # Windows path: C:\Users\<User>\AppData\Local\Microsoft\Windows\Fonts
        dest_dir = os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Windows', 'Fonts')
    elif sys.platform == "darwin":
        # macOS path: ~/Library/Fonts
        dest_dir = os.path.expanduser("~/Library/Fonts")
    else:
        # Linux path: ~/.local/share/fonts
        dest_dir = os.path.expanduser("~/.local/share/fonts")
        
    try:
        os.makedirs(dest_dir, exist_ok=True)

        font_name = os.path.basename(src)
        dest = os.path.join(dest_dir, font_name)
        shutil.copy2(src, dest)  # copy2 preserves metadata

        # Windows: register font in the registry so apps can discover it
        if sys.platform == "win32":
            import winreg
            key_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
                winreg.SetValueEx(key, font_name, 0, winreg.REG_SZ, dest)

        # Linux: refresh font cache so the font is immediately available
        elif sys.platform not in ("win32", "darwin"):
            subprocess.run(["fc-cache", "-f", dest_dir], check=False)

        print(f"Font installed successfully: {dest}")
        return True

    except PermissionError:
        print(f"Error: Permission denied when installing to {dest_dir}")
    except OSError as e:
        print(f"Error: Could not install font: {e}")

    return False