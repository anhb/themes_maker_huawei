from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx


if __name__ == "__main__":

    # Load the original video
    main_path = "assets/live_wallpapers/nebula/sources"
    or_video_name = "v_nebula_1920x1080_original.mp4"
    or_video_path = f"{main_path}/{or_video_name}"

    new_video_name = "output_v_nebula_1920x1080_original.mp4"
    new_video_path = f"{main_path}/{new_video_name}"

    or_video = VideoFileClip(or_video_path)

    # Reverse the video
    reversed_video = or_video.fx(vfx.time_mirror)

    # Concatenate the original and reversed clips
    concatenated_clip = concatenate_videoclips([or_video, reversed_video])

    # Calculate the factor to speed up the video to reduce its duration to 5 seconds
    speed_up_factor = concatenated_clip.duration / 5

    # Speed up the video
    final_video = concatenated_clip.fx(vfx.speedx, speed_up_factor)

    # Write the result to a file
    final_video.write_videofile(new_video_path)