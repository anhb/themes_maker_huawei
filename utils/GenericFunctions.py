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
def rename_file_dir(src, dst):
    try:
        os.rename(src, dst)
        print(f"Renamed file '{src}' to '{dst}'")
    except OSError as error:
        print(f"Error: {error}")


# Copy a dir or file
def copy_dir_or_file(src, dst):
    # If the destination directory exists, shutil.copytree will fail. So, handle it.
    if os.path.exists(dst):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)  # For directories, copy recursively
                print(f"Dir copied from: '{s}' to '{d}'")
            else:
                shutil.copy2(s, d)  # For files, use copy2 to preserve metadata
                print(f"File copied from: '{s}' to '{d}'")
    else:
        # If the destination directory does not exist, use copytree normally
        shutil.copytree(src, dst, dirs_exist_ok=True)


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


def list_dirs(path):
    # List all entries in the directory given by "path"
    entries = os.listdir(path)

    # Use list comprehension to filter out directories
    directories = [entry for entry in entries if os.path.isdir(os.path.join(path, entry))]

    return directories


""" Icon Donwload """


def download_icon_logo_from_playstore(package_name, path_write, name_logo):
    url = f"https://play.google.com/store/apps/details?id={package_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    img_tag = soup.find('img', {'class': 'T75of cN0oRe fFmL2e'})

    if img_tag and 'src' in img_tag.attrs:
        logo_url = img_tag['src']
        print(f"Logo URL: {logo_url}")
        # Optionally download the image
        img_response = requests.get(logo_url)
        with open(f"{path_write}/{name_logo}", 'wb') as file:
            file.write(img_response.content)
        print(f"Logo downloaded in {path_write}/{name_logo}")
    else:
        print("Logo not found.")


""" Image Manipulation """


def get_image_size(image_path):
    path_parts = image_path.split(os.path.sep)
    with Image.open(image_path) as img:
        if len(path_parts) >= 3:  # Ensure the path is long enough
            print(f"{path_parts[-2]}: {img.size[0]}x{img.size[1]} (width x height)")
        return img.size


def resize_image(image_path, new_size):
    with Image.open(image_path) as img:
        return img.resize(new_size, Image.Resampling.LANCZOS)


def crop_to_shape(image_path, output_path, shape):
    with Image.open(image_path) as img:
        # Resize to a square based on the shortest side to maintain aspect ratio
        img_rgb = img.convert('RGBA')
        side_length = min(img_rgb.size)
        img = img_rgb.resize((side_length, side_length), Image.Resampling.LANCZOS)
        # Create a mask
        mask = Image.new('L', (side_length, side_length), 0)
        draw = ImageDraw.Draw(mask)

        if shape == 'circle':
            draw.ellipse([(0, 0), (side_length, side_length)], fill=255)

        elif shape == 'hexagon':
            # Coordinates for a hexagon
            coords = [(
                side_length * 0.5 + side_length * 0.5 * math.cos(2 * math.pi * i / 6),
                side_length * 0.5 + side_length * 0.5 * math.sin(2 * math.pi * i / 6)
            ) for i in range(6)]
            draw.polygon(coords, fill=255)

        elif shape == 'octagon':
            # Coordinates for a octagon
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


def extract_all_colors(image_path):
    with Image.open(image_path) as img:
        img = img.convert('RGB')  # Ensure image is in RGB format
        colors = img.getcolors(maxcolors=1024 * 1024)  # Get colors from the image

        # If the image has too many colors, this might return None
        if colors is None:
            print("Too many colors in the image to count.")
            return

        # Count and sort the colors
        counter = Counter({color: count for count, color in colors})
        return counter


def black_and_white(input_image_path, output_image_path):
    color_image = Image.open(input_image_path)
    bw = color_image.convert('L')
    bw.save(output_image_path)


def black_and_white_dithering(input_image_path, output_image_path, dithering=True):
    color_image = Image.open(input_image_path)
    if dithering:
        bw = color_image.convert('1')
    else:
        bw = color_image.convert('1', dither=Image.NONE)
    bw.save(output_image_path)


def divided_range(divisions, start=0, end=255):
    range_size = end - start
    segment_size = range_size / divisions

    segments = []
    for i in range(divisions):
        segment_start = start + i * segment_size
        segment_end = segment_start + segment_size
        if i == divisions - 1:  # Ensure the last segment ends at the 'end'
            segment_end = end
        segments.append((segment_start, segment_end))

    return segments


def categorized_custom_num_color(segment_start, segment_end, index, rgb):
    r, g, b = rgb
    if r == g == b:  # Ensure it's a grayscale color
        if r >= segment_start and r <= segment_end:
            color = f"color_{index}"
            # print(f"{color}: {rgb}")
            return color
        else:
            return None


def get_custom_categorized_ex_colors(extracted_colors, num_colors_to_extract):
    # Segment ranges by the number of colors to extract
    segments = divided_range(num_colors_to_extract)

    categorized_colors = {}
    for rgb in extracted_colors.keys():
        for i, (start, end) in enumerate(segments):
            tmp = categorized_custom_num_color(start, end, i, rgb)
            if tmp != None:
                categorized_colors.update({rgb: tmp})

    return categorized_colors


def replace_custom_colors(image_path, output_path, new_colors, extracted_custom_colors):
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        pixels = img.load()

        for i in range(img.width):
            for j in range(img.height):
                category = extracted_custom_colors[pixels[i,j]]
                new_color = new_colors[category]
                pixels[i,j] = new_color

        img.save(output_path)


def print_segment_ranges(segments):
    for i, (start, end) in enumerate(segments):
        print(f"Segment {i + 1}: Start = {start}, End = {end}")


def categorize_color(rgb):
    r, g, b = rgb
    if r == g == b:
        return "Gray"
    elif r < 10 and g < 10 and b < 10:
        return "Black"
    elif r > 245 and g > 245 and b > 245:
        return "White"
    else:
        return "Other"


def categorize_grayscale_color(rgb):
    r, g, b = rgb
    if r == g == b:  # Ensure it's a grayscale color
        if r <= 50:  # Low values are black 50
            return "Black"
        elif r >= 220:  # High values are white 220
            return "White"
        else:
            return "Gray"
    else:
        return "Not Grayscale"


def replace_colors(image_path, output_path, black_replace, white_replace, gray_replace):
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        pixels = img.load()

        for i in range(img.width):
            for j in range(img.height):
                category = categorize_grayscale_color(pixels[i, j])
                if category == "Black":
                    pixels[i, j] = black_replace
                elif category == "White":
                    pixels[i, j] = white_replace
                elif category == "Gray":
                    pixels[i, j] = gray_replace

        img.save(output_path)

