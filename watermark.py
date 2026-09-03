import subprocess
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_duration(file_path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", file_path],
        capture_output=True, text=True
    )
    return float(result.stdout.strip())

def add_watermark(input_file, output_file,
                   username="MARCO",
                   start_duration=10, end_duration=10,
                   fontfile=None,
                   logo_png=None):
    if fontfile is None:
        fontfile = os.path.join(BASE_DIR, "font.otf")
    if logo_png is None:
        logo_png = os.path.join(BASE_DIR, "logo.png")

    print(f"DEBUG: logo_png path = {logo_png}, exists = {os.path.exists(logo_png)}")
    print(f"DEBUG: fontfile path = {fontfile}, exists = {os.path.exists(fontfile)}")

    duration = get_duration(input_file)
    end_start = duration - end_duration

    cmd = [
        "ffmpeg", "-y",
        "-i", input_file,
        "-i", logo_png,
        "-filter_complex",
        (
            f"[1:v]scale=80:80[logo];"
            f"[0:v][logo]overlay=(W-w)/2:(H-h)/2-40:"
            f"enable='between(t,0,{start_duration})+between(t,{end_start},{duration})'[v1];"
            f"[v1]drawtext=fontfile={fontfile}:text='{username}':"
            f"fontcolor=white@0.5:fontsize=26:"
            f"x=(w-text_w)/2:y=(h-text_h)/2+30:"
            f"shadowcolor=black@0.6:shadowx=2:shadowy=2:"
            f"enable='between(t,0,{start_duration})+between(t,{end_start},{duration})'"
        ),
        "-codec:a", "copy",
        output_file
    ]

    subprocess.run(cmd, check=True)
    return output_file
