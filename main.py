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


def compress_images(folder_selected, target_resolution=1920, target_quality=4):
    """
    Compresses image files in a specified folder, excluding any in a 'Compressed' subfolder.

    Args:
        folder_selected (Path): Path object to the folder containing the images to be compressed.
        target_resolution (int): The target resolution for the compressed images. Defaults to 1920.
        target_quality (int): The target quality for the compressed images (1-31, 1 is the best). Defaults to 4.
    """
    ffmpeg_path = get_ffmpeg_path()

    path_compressed = folder_selected / "Compressed"
    if not path_compressed.exists():
        path_compressed.mkdir()

    for file in folder_selected.iterdir():
        if file.is_dir() or file.suffix.lower() not in [".jpg", ".jpeg", ".png"]:
            continue

        original_file_path = str(file)
        target_file_path = str(path_compressed / file.name)

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

        compress_images(folder_selected_path)
        os.startfile(str(folder_selected_path / "Compressed"))
        print("Compression complete.")

    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")


if __name__ == "__main__":

    keep_running = True

    while keep_running:
        compress_folder()
        keep_running = input("Press Enter to compress another folder, or type 'q' to quit...") != "q"
