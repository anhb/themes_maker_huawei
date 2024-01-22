import os, shutil, json, requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageOps
from collections import Counter
import math


"""JSON Fuctions"""


# print json object in a pretty way
def print_pretty_json(obj):
    conf_json_format = json.dumps(obj, indent=2)
    print(conf_json_format)
    return 0


"""OS Functions"""


# Make only one dir
def make_dir(path):
    try:
        os.mkdir(path)
        print(f"Directory '{path}' created")
    except FileExistsError:
        print(f"Directory '{path}' already exists")


# Make all path if the directories are not exist
def make_dirs(path):
    try:
        os.makedirs(path, exist_ok=True)
        print(f"Nested directories '{path}' created")
    except OSError as error:
        print(f"Creation of the directory '{path}' failed due to: {error}")


# Remove an empty dir
def remove_dir(path):
    try:
        os.rmdir(path)
        print(f"Directory '{path}' removed")
    except OSError as error:
        print(f"Error: {error} - {path}")


# Remove a dir and all its contents
def remove_all(path):
    try:
        shutil.rmtree(path)
        print(f"Directory '{path}' and all its contents removed")
    except OSError as error:
        print(f"Error: {error} - {path}")


# Rename a file or dir
def rename_file_dir(main_path, old_name, new_name):
    curr_nm = f"{main_path}/{old_name}"
    new_nm = f"{main_path}/{new_name}"
    try:
        os.rename(curr_nm, new_nm)
        print(f"Renamed file '{curr_nm}' to '{new_nm}'")
    except OSError as error:
        print(f"Error: {error}")


# Verify if a dir or file exists
def verify_file_dir_exists(path):
    if os.path.exists(path):
        print(f"This '{path}' exists")
        return 0
    else:
        print(f"This '{path}' does not exist")
        return 1


# Print all contents from a specific path
def list_all_content_from_path(path):
    for root, dirs, files in os.walk(path):
        # Print all directories
        for dir_name in dirs:
            print("Directory:", os.path.join(root, dir_name))

        # Print all files
        for file_name in files:
            print("File:", os.path.join(root, file_name))


""" Icon Donwload """


def get_icon_logo_from_playstore(icon_name, path_write):
    url = f"https://play.google.com/store/apps/details?id={icon_name}"
    print(url)
    response = requests.get(url)
    print(response)
    soup = BeautifulSoup(response.content, 'lxml')
    print(soup)
    img_tag = soup.find('img', {'class': 'T75of cN0oRe fFmL2e'})
    print(img_tag)

    if img_tag and 'src' in img_tag.attrs:
        logo_url = img_tag['src']
        print(f"Logo URL: {logo_url}")
        # Optionally download the image
        img_response = requests.get(logo_url)
        with open(f"{path_write}/app_logo.png", 'wb') as file:
            file.write(img_response.content)
        print(f"Logo downloaded in {path_write}")
    else:
        print("Logo not found.")


""" Image Manipulation """


def get_image_size(image_path):
    with Image.open(image_path) as img:
        return img.size


def print_image_size(app_name, image_size):
    print(f"{app_name}: {image_size[0]}x{image_size[1]} (width x height)")


def resize_image(image_path, new_size):
    with Image.open(image_path) as img:
        return img.resize(new_size, Image.Resampling.LANCZOS)


def crop_to_shape(image_path, output_path, shape):
    with Image.open(image_path) as img:
        # Resize to a square based on the shortest side to maintain aspect ratio
        side_length = min(img.size)
        img = img.resize((side_length, side_length), Image.Resampling.LANCZOS)
        # Create a mask
        mask = Image.new('L', (side_length, side_length), 0)
        draw = ImageDraw.Draw(mask)

        if shape == 'circle':
            draw.ellipse([(0, 0), (side_length, side_length)], fill=255)

        elif shape == 'hexagon':
            # Coordinates for a heptagon
            coords = [(
                side_length * 0.5 + side_length * 0.5 * math.cos(2 * math.pi * i / 6),
                side_length * 0.5 + side_length * 0.5 * math.sin(2 * math.pi * i / 6)
            ) for i in range(6)]
            draw.polygon(coords, fill=255)

        elif shape == 'octagon':
            # Coordinates for a heptagon
            coords = [(
                side_length * 0.5 + side_length * 0.5 * math.cos(2 * math.pi * i / 8),
                side_length * 0.5 + side_length * 0.5 * math.sin(2 * math.pi * i / 8)
            ) for i in range(8)]
            draw.polygon(coords, fill=255)
        else:
            print("That shape doesn't exist")

    # Apply the mask and convert to 'RGBA' to add an alpha channel
    result = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
    result.putalpha(mask)

    # Save the result with transparency
    result.save(output_path, format="PNG")


def save_image(image_obj, image_outpath):
    image_obj.save(image_outpath, format="PNG")
    print(f"image saved: {image_outpath}")


def check_image_mode(image_path):
    with Image.open(image_path) as img:
        return img.mode


def extract_colors(image_path, max_colors=10):
    with Image.open(image_path) as img:
        img = img.convert('RGBA')  # Ensure image is in RGB format
        colors = img.getcolors(maxcolors=1024 * 1024)  # Get colors from the image

        # If the image has too many colors, this might return None
        if colors is None:
            print("Too many colors in the image to count.")
            return

        # Count and sort the colors
        counter = Counter({color: count for count, color in colors})
        most_common = counter.most_common(max_colors)

        return most_common