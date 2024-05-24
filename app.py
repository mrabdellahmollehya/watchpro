import sys
import subprocess

if len(sys.argv) != 3:
    print("Usage: python app.py <input_video_url> <rtmp_output_url>")
    sys.exit(1)

input_video_url = sys.argv[1]
rtmp_output_url = sys.argv[2]

cmd = [
    "ffmpeg",
    "-i", input_video_url,
    "-i", "logo.png",
    "-filter_complex", "[1:v]scale=120:-1[logo];[0:v][logo]overlay=40:H-h-40[out]",
    "-map", "[out]",
    "-map", "0:a",
    "-c:v", "libx264",
    "-b:v", "2500k",
    "-c:a", "aac",
    "-f", "flv",
    rtmp_output_url
]

subprocess.run(cmd)
