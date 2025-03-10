from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox


def compress_jpg(input_path, output_path, quality=50, max_size=None):
    """
    Compresses a JPG image by reducing quality and optionally resizing it,
    ensuring that the final file size is at least 1MB.

    :param input_path: Path to the input JPG file
    :param output_path: Path to save the compressed JPG file
    :param quality: Quality level (1-100, lower means more compression)
    :param max_size: Tuple (max_width, max_height) to resize (optional)
    """
    try:
        with Image.open(input_path) as img:
            if max_size:
                img.thumbnail(max_size)  # Resize while maintaining aspect ratio

            # Start with given quality, then adjust to meet the 1MB size constraint
            current_quality = quality
            while True:
                img.save(output_path, 'JPEG', quality=current_quality, optimize=True)
                if os.path.getsize(output_path) >= 1 * 1024 * 1024 or current_quality >= 95:
                    break
                current_quality += 5  # Increase quality stepwise if file is too small

            messagebox.showinfo("Success",
                                f"Compressed image saved as {output_path}, Size: {os.path.getsize(output_path) / 1024:.2f} KB")
    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")


def select_files():
    root = tk.Tk()
    root.withdraw()
    input_files = filedialog.askopenfilenames(title="Select JPG Files", filetypes=[("JPG files", "*.jpg;*.jpeg")])
    if not input_files:
        return

    output_folder = filedialog.askdirectory(title="Select Output Folder")
    if not output_folder:
        return

    quality = simpledialog.askinteger("Quality", "Enter quality (1-100)", minvalue=1, maxvalue=100, initialvalue=50)
    max_width = simpledialog.askinteger("Max Width", "Enter max width (optional, leave blank for no resize)",
                                        minvalue=1) or None
    max_height = simpledialog.askinteger("Max Height", "Enter max height (optional, leave blank for no resize)",
                                         minvalue=1) or None
    max_size = (max_width, max_height) if max_width and max_height else None

    for input_file in input_files[:1000]:
        output_file = f"{output_folder}/{os.path.basename(input_file)}"
        compress_jpg(input_file, output_file, quality, max_size)


if __name__ == "__main__":
    select_files()