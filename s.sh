#!/bin/bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input_video_url> <rtmp_output_url>"
    exit 1
fi

INPUT_VIDEO_URL="$1"
RTMP_OUTPUT_URL="$2"

# Run ffmpeg with the provided arguments
ffmpeg -i "${INPUT_VIDEO_URL}" -i logo.png -filter_complex "[1:v]scale=120:-1[logo];[0:v][logo]overlay=40:H-h-40[out]" -map "[out]" -map 0:a -c:v libx264 -b:v 2500k -c:a aac -f flv "${RTMP_OUTPUT_URL}"
