from tkinter import filedialog, Tk
from pathlib import Path

from PIL import Image


def compress_images(file, target_resolution=1920, target_quality=60):
    """
    Compresses an image file to a specified resolution and quality.

    Args:
        file (Path): The file to compress.
        target_resolution (int): The target width resolution for the compressed images. Defaults to 1920.
        target_quality (int): The target quality for the compressed images (0-100, 100 is the best). Defaults to 85.
    """
    original_image = Image.open(file)

    # Calculate the target height to maintain aspect ratio
    aspect_ratio = original_image.height / original_image.width
    target_height = int(target_resolution * aspect_ratio)

    # Resize the image
    resized_image = original_image.resize((target_resolution, target_height))

    # Create the folder for the compressed images if it doesn't exist
    target_folder = file.parent / "Compressed"
    target_folder.mkdir(parents=True, exist_ok=True)

    # Save the image in JPEG format
    target_file_path = target_folder / file.with_suffix('.jpg').name
    resized_image.save(target_file_path, format='JPEG', quality=target_quality, optimize=True)
    print(f"Compressed {file.name}")


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
