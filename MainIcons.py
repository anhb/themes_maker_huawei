from settings.ConfigLoader import ConfigLoader
from settings.LoadVariables import LoadVariables
from utils.GenericFunctions import (print_pretty_json, make_dir, make_dirs, remove_dir, remove_all, rename_file_dir,
                                    verify_file_dir_exists, list_all_content_from_path, download_icon_logo_from_playstore,
                                    get_image_size, resize_image, save_image, check_image_mode, divided_range,
                                    extract_all_colors, crop_to_shape, black_and_white, black_and_white_dithering,
                                    categorize_color, categorize_grayscale_color, replace_colors, copy_dir_or_file,
                                    list_dirs, print_segment_ranges, categorized_custom_num_color,
                                    get_custom_categorized_ex_colors, replace_custom_colors)


def get_all_app_names(l_application):
    app_names = []
    for app_name in l_application:
        app_names.append(app_name)
    return app_names


def get_all_package_names(list_all_apps, l_application):
    package_names = []
    for app_name in list_all_apps:
        package_names.append(l_application[app_name]["package_name"])
    return package_names


def get_app_package_name(app_name, l_application):
    return l_application[app_name]["package_name"]


def validate_existing_app(app_validate, list_all_apps):
    if app_validate in list_all_apps:
        print(f"{app_validate} is in the list.")
    else:
        print(f"{app_validate} is not in the list.")


def copy_not_working_apps(icon_not_working_path, icon_path):
    l_nw_paths = list_dirs(icon_not_working_path)
    for dir_name in l_nw_paths:
        path_src = f"{icon_not_working_path}/{dir_name}"
        path_dst = f"{icon_path}/{dir_name}"
        copy_dir_or_file(path_src, path_dst)


def download_multiple_icon_logos_from_playstore(l_application, icon_path, name_logo):
    app_names = get_all_app_names(l_application)
    for app_name in app_names:
        path_dir_app_name = f"{icon_path}/{app_name}"
        print(f"=========={app_name}==========")
        make_dir(path_dir_app_name)
        package_name = get_app_package_name(app_name, l_application)
        download_icon_logo_from_playstore(package_name, path_dir_app_name, name_logo)


def print_all_image_sizes(application_names, icon_path, name_logo):
    for app_name in application_names:
        path_app_logo = f"{icon_path}/{app_name}/{name_logo}"
        get_image_size(path_app_logo)


def get_variable_new_size_format(new_size):
    return (new_size, new_size)


def resize_multiple_images(application_names, icon_path, dflt_name_logo, new_size, icon_format):
    for app_name in application_names:
        path_app_logo = f"{icon_path}/{app_name}/{dflt_name_logo}"
        new_img = resize_image(path_app_logo, new_size)
        new_path_app_logo = f"{dflt_name_logo}_{new_size[0]}x{new_size[1]}.{icon_format}"
        output_path = f"{icon_path}/{app_name}/{new_path_app_logo}"
        save_image(new_img, output_path)


def crop_all_pictures(application_names, icon_path, dflt_name_logo, icon_style, icon_format):
    for app_name in application_names:
        path_app_logo = f"{icon_path}/{app_name}/{dflt_name_logo}"
        print(path_app_logo)
        path_new_circle_logo = f"{icon_path}/{app_name}/{icon_dflt_name}_{icon_style}.{icon_format}"
        print(path_new_circle_logo)
        crop_to_shape(path_app_logo, path_new_circle_logo, icon_style)


def change_to_bw_all_pictures(application_names, icon_path, dflt_name_logo, icon_bw, icon_format):
    for app_name in application_names:
        path_app_logo = f"{icon_path}/{app_name}/{dflt_name_logo}"
        print(path_app_logo)
        path_new_bw_logo = f"{icon_path}/{app_name}/{icon_dflt_name}_{icon_bw}.{icon_format}"
        print(path_new_bw_logo)
        black_and_white(path_app_logo, path_new_bw_logo)


def change_to_bw_dithering_all_pictures(application_names, icon_path, dflt_name_logo, icon_bw_d, icon_format):
    for app_name in application_names:
        path_app_logo = f"{icon_path}/{app_name}/{dflt_name_logo}"
        print(path_app_logo)
        path_new_bw_logo = f"{icon_path}/{app_name}/{icon_dflt_name}_{icon_bw_d}.{icon_format}"
        print(path_new_bw_logo)
        black_and_white_dithering(path_app_logo, path_new_bw_logo)


if __name__ == "__main__":

    """ Main Variables:
    - load_variables: Instance LoadVariables (Get all values from JSON)
    
    - icon_path: Path where you are going to manage all icons
    - icon_not_working_path: Path where all icons that are not working for downloading are there
    - icon_dflt_name: File name for the original logo.png
    """
    load_variables = LoadVariables(ConfigLoader().get_config())

    icon_path = load_variables.icon_path
    # print(icon_path)

    icon_not_working_path = load_variables.icon_not_working_path
    # print(icon_not_working_path)

    icon_dflt_name = load_variables.icon_default_name
    # print(icon_dflt_name)

    """ Main Array variables:
    - all_app_names: Get an array with all application names
    - all_packages_names: Get an array with all package names 
    """
    all_app_names = get_all_app_names(load_variables.l_application)
    # print(l_app_names)

    all_package_names = get_all_package_names(all_app_names, load_variables.l_application)
    # print(l_package_names)

    """ Custom Variables for single functions that you can modify to execute a specific process:
    - app_name: Name of the app
    - icon_size: Size of a picture that you going to use, normally this change to a format (ex: 192x192)
    - icon_format: Image format that you are going to work with
    - icon_style: Image style that you are going to cut the ops are: 'circle', 'hexagon', 'octagon' 
    """
    app_name = "facebook"
    icon_size = 192
    icon_format = "png"
    icon_style = "circle"
    icon_bw = "bw"
    icon_bw_d = "bwd"

    """ Variables made from custom variables that you are going to use in the process:
    - icon_dflt_name_format: File name with format for the original logo
    - path_dir_single_app: Path for a specific app
    - package_name: Package name from a specific app name
    - path_single_app_logo: Path for the specific default logo
    - path_new_circle_logo: Path for the specific with circle or style logo
    - path_bw_single_app_logo: Path for the specific black and white logo
    - path_bw_d_single_app_logo: Path for the specific black and white with dithering logo
    """
    icon_dflt_name_format = f"{icon_dflt_name}.{icon_format}"
    # print(icon_dflt_name_format)

    path_dir_app = f"{icon_path}/{app_name}"
    # print(path_dir_single_app)

    package_name = get_app_package_name(app_name, load_variables.l_application)
    # print(package_name)

    path_single_app_logo = f"{path_dir_app}/{icon_dflt_name_format}"
    # print(path_single_app_logo)

    path_new_circle_logo = f"{path_dir_app}/{icon_dflt_name}_{icon_style}.{icon_format}"
    # print(path_new_circle_logo)

    path_bw_single_app_logo = f"{path_dir_app}/{icon_dflt_name}_{icon_bw}.{icon_format}"
    # print(path_bw_single_app_logo)

    path_bw_d_single_app_logo = f"{path_dir_app}/{icon_dflt_name}_{icon_bw_d}.{icon_format}"
    # print(path_bw_d_single_app_logo)

    """ All main functions that you are going to use for a single app
    """

    ## Validate if exists an app
    # validate_existing_app(app_name, all_app_names)

    ## Create first 'apps' directory on assets
    # make_dir(icon_path)

    ## Copy dir or file for apps_not_working
    # copy_not_working_apps(icon_not_working_path, icon_path)

    ## Download single logo from app_name
    # download_icon_logo_from_playstore(package_name, path_dir_single_app, icon_dflt_name_format)

    ## Print and get size from a picture
    # logo_size = get_image_size(path_single_app_logo)
    ## Resize image
    new_size = get_variable_new_size_format(icon_size)
    img_obj = resize_image(path_single_app_logo, new_size)
    ## Save resized image
    # print(img_obj.size)
    # new_logo_name_resized = f"{icon_dflt_name}_{new_size[0]}x{new_size[1]}.{icon_format}"
    # new_path_resized_app = f"{path_dir_app}/{new_logo_name_resized}"
    # save_image(img_obj, new_path_resized_app)

    ## Cut picture for a specific shape

    # crop_to_shape(path_single_app_logo, path_new_circle_logo, icon_style)

    ## Change single picture to gray scale (black and white)
    # black_and_white(path_single_app_logo, path_bw_single_app_logo)
    # black_and_white_dithering(path_single_app_logo, path_bw_d_single_app_logo)

    """ All main functions that you are going to use for multiple apps:
    """
    ## Download the all logos from the configurations
    # download_multiple_icon_logos_from_playstore(load_variables.l_application, icon_path, icon_dflt_name_format)

    ## Rename files or dirs
    # src = "" # file or dir
    # dst = "" # file or dir
    # rename_file_dir(src, dst)

    ## Print and get size from all pictures
    # print_all_image_sizes(all_app_names, icon_path, icon_dflt_name_format)
    ## Resize all images
    # resize_multiple_images(all_app_names, icon_path, icon_dflt_name_format, new_size, icon_format)

    ## Cut all pictures for a specific shape
    # crop_all_pictures(all_app_names, icon_path, icon_dflt_name_format, icon_style, icon_format)

    ## Change all pictures to gray scale (black and white)
    # change_to_bw_all_pictures(all_app_names, icon_path, icon_dflt_name_format, icon_bw, icon_format)
    # change_to_bw_dithering_all_pictures(all_app_names, icon_path, icon_dflt_name_format, icon_bw_d, icon_format)


    ## Extract colors from a picture
    ex_colors_array = extract_all_colors(path_bw_single_app_logo)
    print(f"{ex_colors_array}")

    ## Extract specific range of colors from picture
    numcolors = 2  # Num of colors to extract
    ex_custom_range_colors = get_custom_categorized_ex_colors(ex_colors_array, numcolors)
    print(ex_custom_range_colors)

    ## Replace colors from picture using specific range
    ## Color 0 -> means for colors near to black
    ## Colors greater -> means for colors near to white

    # Facebook
    new_colors = {
        "color_0": (12, 53, 106),
        "color_1": (238, 245, 255)
    }

    print(new_colors)
    # path_new_color_logo = f"{path_dir_app}/{icon_dflt_name}_newest.{icon_format}"
    # replace_custom_colors(path_bw_single_app_logo, path_new_color_logo, new_colors, ex_custom_range_colors)

    for app_name in all_app_names:
        path_app_bw = f"{icon_path}/{app_name}/{icon_dflt_name}_{icon_bw}.{icon_format}"
        path_new_color_logo = f"assets/icons/logos_tmp/{app_name}_{icon_dflt_name_format}"
        ex_colors_array = extract_all_colors(path_app_bw)
        ex_custom_range_colors = get_custom_categorized_ex_colors(ex_colors_array, numcolors)
        replace_custom_colors(path_app_bw, path_new_color_logo, new_colors, ex_custom_range_colors)

    # print_segment_ranges(segments)
    """
    categorized_colors = {}
    for rgb in ex_colors_array.keys():
        for i, (start, end) in enumerate(segments):
            tmp = categorized_color_segment(start, end, i, rgb)
            if tmp != None:
                categorized_colors.update({rgb: tmp})

    print(categorized_colors)

    #for i, (start, end) in enumerate(segments):
    #    categorized_color_segment(start, end, i)
    """

    """
    categorized = {rgb: categorize_grayscale_color(rgb) for rgb in ex_colors_array.keys()}
    #categorized = {rgb: categorize_color(rgb) for rgb in ex_colors_array.keys()}
    #categorized = [(rgb, count, categorize_color(rgb)) for rgb, count in ex_colors_array]
    unique_color_names = list(set(color[1] for color in categorized.items()))
    print(unique_color_names)
    print(f"{categorized}")

    out_baw_path = "/home/bleakmurder/IdeaProjects/themes_maker_huawei/assets/icons/apps/facebook/app_logo_BW_result.png"
    # Pasar imagen a escala de grises
    black_replace = (255, 0, 0)  # Replace black with red
    white_replace = (238, 245, 255)  # Replace white with green
    gray_replace = (12, 53, 106)
    replace_colors(in_baw_path, out_baw_path, black_replace, white_replace, gray_replace)
    """


    """
    # Check image color mode
    icon_default_name = load_variables.icon_default_name
    for app_name in l_app_names:
        path_app_logo = f"{icon_path}/{app_name}/{icon_default_name}"
        # check image color mode
        #print(f"{app_name}: {check_image_mode(path_app_logo)}")
        # Check image color mode and their count value
        print(f"{app_name} ({check_image_mode(path_app_logo)}): {extract_colors(path_app_logo, 20)}")
        #print(f"{app_name} ({check_image_mode(path_app_logo)}): {extract_hex_colors(path_app_logo, 1000)}")
    """