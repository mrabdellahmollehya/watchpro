# Use the official Ubuntu image as the base image
FROM ubuntu:20.04

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Set the working directory
WORKDIR /app

# Copy the shell script and logo file into the container
COPY s.sh .
COPY logo.png .

# Make the shell script executable
RUN chmod +x s.sh

# Set the command to run the script with environment variables
CMD ["sh", "-c", "./s.sh \"$INPUT_VIDEO_URL\" \"$RTMP_OUTPUT_URL\""]
