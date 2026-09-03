import subprocess

def get_duration(file_path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", file_path],
        capture_output=True, text=True
    )
    return float(result.stdout.strip())

def add_watermark(input_file, output_file,
                   username="MICHAEL",
                   start_duration=10, end_duration=10,
                   fontfile="font.otf",
                   emoji_font="NotoColorEmoji.ttf"):
    duration = get_duration(input_file)
    end_start = duration - end_duration

    cmd = [
        "ffmpeg", "-y",
        "-i", input_file,
        "-vf", (
            f"drawtext=fontfile={emoji_font}:text='💀':"
            f"fontsize=40:fontcolor=white@0.7:"
            f"x=(w-text_w)/2:y=(h-text_h)/2-30:"
            f"enable='between(t,0,{start_duration})+between(t,{end_start},{duration})',"
            f"drawtext=fontfile={fontfile}:text='{username}':"
            f"fontcolor=white@0.5:fontsize=26:"
            f"x=(w-text_w)/2:y=(h-text_h)/2+20:"
            f"shadowcolor=black@0.6:shadowx=2:shadowy=2:"
            f"enable='between(t,0,{start_duration})+between(t,{end_start},{duration})'"
        ),
        "-codec:a", "copy",
        output_file
    ]

    subprocess.run(cmd, check=True)
    return output_file
