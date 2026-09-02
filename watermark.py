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
                   fontfile="font.otf"):
    duration = get_duration(input_file)
    end_start = duration - end_duration

    cmd = [
        "ffmpeg", "-y",
        "-i", input_file,
        "-vf", (
            f"drawtext=fontfile={fontfile}:text='{username}':"
            f"fontcolor=white:fontsize=28:x=10:y=10:"
            f"box=1:boxcolor=black@0.5:boxborderw=5:"
            f"enable='between(t,0,{start_duration})+between(t,{end_start},{duration})'"
        ),
        "-codec:a", "copy",
        output_file
    ]

    subprocess.run(cmd, check=True)
    return output_file