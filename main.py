import os
import subprocess
from tkinter import filedialog, Tk
from pathlib import Path
import sys


def get_ffmpeg_path():
    # Check if we are running as a PyInstaller bundle
    if getattr(sys, 'frozen', False):
        # If bundled, the executable path is in _MEIPASS
        bundle_dir = Path(sys._MEIPASS)
    else:
        # If running normally, use the script's directory
        bundle_dir = Path(__file__).parent

    ffmpeg_path = bundle_dir / "ffmpeg.exe"
    return ffmpeg_path


def compress_images(file, target_resolution=1920, target_quality=4):
    """
    Compresses image files in a specified folder, excluding any in a 'Compressed' subfolder.

    Args:
        file (Path): The file to compress.
        target_resolution (int): The target resolution for the compressed images. Defaults to 1920.
        target_quality (int): The target quality for the compressed images (1-31, 1 is the best). Defaults to 4.
    """
    ffmpeg_path = get_ffmpeg_path()

    original_file_path = str(file)
    target_file_path = str(file.parent / "Compressed" / file.name)

    # Create the folder for the compressed images if it doesn't exist
    Path(file.parent / "Compressed").mkdir(parents=True, exist_ok=True)

    command = [
        str(ffmpeg_path), "-y", "-i", original_file_path,
        "-vcodec", "mjpeg", "-vf", f"scale={target_resolution}:-1",
        "-q:v", str(target_quality), target_file_path
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Compressed {file.name}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to compress {file.name}: {e}")


def compress_folder():
    try:
        print("Select the folder with the photos you want to compress:")
        root = Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        folder_selected = filedialog.askdirectory()

        if not folder_selected:
            print("No folder selected! Exiting.")
            exit()

        folder_selected_path = Path(folder_selected)

        compress_images_recursive(folder_selected_path)
        # os.startfile(str(folder_selected_path / "Compressed"))

    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")


def compress_images_recursive(folder):
    for item in folder.iterdir():
        if item.is_dir() and item.name != "Compressed":
            compress_images_recursive(item)
        elif item.is_file() and item.suffix.lower() in [".jpg", ".jpeg", ".png"]:
            compress_images(item)


if __name__ == "__main__":
    keep_running = True

    while keep_running:
        compress_folder()
        keep_running = input("Press Enter to compress another folder, or type 'q' to quit...") != "q"
