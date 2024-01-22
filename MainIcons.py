from settings.ConfigLoader import ConfigLoader
from settings.LoadVariables import LoadVariables
from utils.GenericFunctions import (print_pretty_json, make_dir, make_dirs, remove_dir, remove_all, rename_file_dir,
                                    verify_file_dir_exists, list_all_content_from_path, get_icon_logo_from_playstore,
                                    get_image_size, print_image_size, resize_image, save_image, check_image_mode,
                                    extract_colors, crop_to_shape)


def get_all_app_names(l_application):
    app_names = []
    for app_name in l_application:
        app_names.append(app_name)
    return app_names


def get_all_icon_names(list_all_apps, l_application):
    icon_names = []
    for app_name in list_all_apps:
        icon_names.append(l_application[app_name]["icon_name"])
    return icon_names


def get_app_icon_name(app_name, l_application):
    return l_application[app_name]["icon_name"]


def get_old_icon_name(brand, app_name, size, format):
    return f"{brand}-{app_name}-{size}.{format}"


def validate_existing_app(app_validate, list_all_apps):
    if app_validate in list_all_apps:
        print(f"{app_validate} is in the list.")
    else:
        print(f"{app_validate} is not in the list.")


def validate_icon_app_before(icon_path, app_name, icon_style, brand, size, format):
    app_path = f"{icon_path}/{app_name}"
    style_path = f"{app_path}/{icon_style}"

    old_icon_name = get_old_icon_name(brand, app_name, size, format)
    old_icon_path = f"{style_path}/{old_icon_name}"

    all_paths = [app_path, style_path, old_icon_path]
    for path in all_paths:
        verify_file_dir_exists(path)


if __name__ == "__main__":

    # Load variables from JSON
    load_variables = LoadVariables(ConfigLoader().get_config())

    """
    print(load_variables.icon_path)
    print(load_variables.l_icon_size)
    print(load_variables.l_icon_style)
    print(load_variables.l_icon_brand)
    print(load_variables.l_icon_format)
    """

    # Get all app names in a array
    l_app_names = get_all_app_names(load_variables.l_application)
    # print(l_app_names)

    # Validate if exists an app
    validate_existing_app("facebook", l_app_names)

    # Get all new icon names
    l_icon_names = get_all_icon_names(l_app_names, load_variables.l_application)
    # print(l_icon_names)

    # Get specific icon_name from app name
    icon_name = get_app_icon_name("facebook", load_variables.l_application)

    # Validate app paths
    app_name = "undostres"
    icon_path = load_variables.icon_path
    icon_style_circle = load_variables.l_icon_style[0]
    icon_brand_icons8 = load_variables.l_icon_brand[0]
    icon_size_192 = load_variables.l_icon_size[0]
    icon_format_png = load_variables.l_icon_format[0]

    validate_icon_app_before(icon_path, app_name, icon_style_circle, icon_brand_icons8, icon_size_192, icon_format_png)
    # print(icon_old_name)

    # List all from path
    # list_all_content_from_path(icon_path)

    #### Get Logo from Playstore
    """
    # Single logo download 
    app_name2 = "undostres"
    path_app_name = f"{icon_path}/{app_name2}"
    icon_name2 = get_app_icon_name(app_name2, load_variables.l_application)
    get_icon_logo_from_playstore(icon_name2, path_app_name)
    """

    """ 
    #All apps logo download
    for app_name in l_app_names:
        path_app_name = f"{icon_path}/{app_name}"
        print(f"=========={app_name}==========")
        make_dir(path_app_name)
        icon_name = get_app_icon_name(app_name, load_variables.l_application)
        get_icon_logo_from_playstore(icon_name, path_app_name)
    """
    # print()

    ### Rename Icons
    """
    # Rename old file
    icon_app_path = f"{icon_path}/{app_name}/{icon_style_circle}/"
    icon_old_name = get_old_icon_name(icon_brand_icons8, app_name, icon_size_192, icon_format_png)
    icon_new_name = get_app_icon_name(app_name, load_variables.l_application)
    rename_file_dir(icon_app_path, icon_old_name, icon_new_name)
    """

    ### Icon Manage
    ## 240x240 normal, 192x192 huawei, third_icons_more_pixel than 240
    """
    # Print all sizes from app logos
    icon_default_name = load_variables.icon_default_name
    for app_name in l_app_names:
        path_app_name = f"{icon_path}/{app_name}/{icon_default_name}"
        print_image_size(app_name, get_image_size(path_app_name))
    
    # Resize app_logo.png
    path_app_logo = f"{icon_path}/undostres/{icon_default_name}"
    new_size = (240,240)
    img_obj = resize_image(path_app_logo, new_size)
    # Make pixels dir
    path_size_logo_dir = f"{icon_path}/undostres/{new_size[0]}x{new_size[1]}"
    make_dir(path_size_logo_dir)
    # Save logo in the pixel dir
    path_output = f"{path_size_logo_dir}/{icon_default_name}"
    save_image(img_obj, path_output)
    """

    icon_default_name = load_variables.icon_default_name
    path_app_logo = f"{icon_path}/facebook/{icon_default_name}"
    path_output = f"{icon_path}/facebook/test6.png"
    # circle, hexagon, octagon,
    crop_to_shape(path_app_logo, path_output, "circle")
    #crop_to_pentagon(path_app_logo, path_output)


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