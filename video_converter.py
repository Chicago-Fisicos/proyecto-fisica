import os
import subprocess


def generate_h264_video(input_video_path, output_video_path):
    # Remove the output file if it already exists
    if os.path.exists(output_video_path):
        os.remove(output_video_path)

    # Set up parameters for the ffmpeg command
    ffmpeg_command = [
        'ffmpeg',
        '-i', input_video_path,
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '23',
        '-c:a', 'aac',
        '-b:a', '128k',
        output_video_path
    ]

    # Execute the ffmpeg command
    subprocess.run(ffmpeg_command)
