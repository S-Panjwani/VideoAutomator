import os
import random
from moviepy.editor import VideoFileClip, ImageClip, TextClip, CompositeVideoClip
from moviepy.config import change_settings
from multiprocessing import Pool

# Set the path to the ImageMagick binary
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})  # Update with your ImageMagick path

# Paths
flags_path = r"C:\Users\panjw_gco4a0t\Documents\GitHub\VideoAutomater\Assets\Flags"
templates_path = r"C:\Users\panjw_gco4a0t\Documents\GitHub\VideoAutomater\Assets\Templates"
output_path = r"C:\Users\panjw_gco4a0t\Documents\GitHub\VideoAutomater\OUTPUT"
required_flags_path = r"C:\Users\panjw_gco4a0t\Documents\GitHub\VideoAutomater\Assets\test"

# Load Templates
template_files = [os.path.join(templates_path, file) for file in os.listdir(templates_path) if file.endswith('.mp4')]

# Load Flags
flag_files = [os.path.join(flags_path, file) for file in os.listdir(flags_path) if file.endswith('.png')]

# Load Required Flags
required_flag_files = [os.path.join(required_flags_path, file) for file in os.listdir(required_flags_path)]

# Optional: Adjust flag size manually (set to None if no resizing is needed)
flag_size = None  # Example: (1080, 1920) for width, height adjustment

# Function to create a video with a specific template and random flags
def create_video(params):
    template_file, video_id, text_fontsize = params
    template_clip = VideoFileClip(template_file)

    # Randomly select two flags
    selected_flags = random.sample(flag_files, 2)

    # Ensure at least one required flag is included
    if required_flag_files:
        required_flag = random.choice(required_flag_files)
        if required_flag not in selected_flags:
            selected_flags.append(required_flag)
            # Shuffle to avoid placing the required flag always in the same position
            random.shuffle(selected_flags)
    
    # Define timestamps
    timestamps = [
        (3.1, 7.8),  # First flag
        (9.04, 13.3), # Second flag
        (14.8, 19.4) # Third flag
    ]
    
    answers_timestamps = [
        (7.9, 8.26),  # First answer
        (13.4, 14.22), # Second answer
        (19.5, 20) # Third answer
    ]

    # Create text and image clips for each flag segment
    segments = [template_clip]

    for i, (flag, timestamp, answer_timestamp) in enumerate(zip(selected_flags, timestamps, answers_timestamps)):
        flag_clip = ImageClip(flag).set_duration(timestamp[1] - timestamp[0])

        if flag_size:
            flag_clip = flag_clip.resize(flag_size)  # Adjust size if needed

        flag_clip = flag_clip.set_position('center').set_start(timestamp[0]).set_end(timestamp[1])

        answer_text = os.path.splitext(os.path.basename(flag))[0]

        # Create the white text (background) slightly larger
        answer_clip_white = (TextClip(answer_text, fontsize=text_fontsize + 10, color='white')
                             .set_duration(answer_timestamp[1] - answer_timestamp[0])
                             .set_position('center')
                             .set_start(answer_timestamp[0])
                             .set_end(answer_timestamp[1]))

        # Create the black text (foreground)
        answer_clip_black = (TextClip(answer_text, fontsize=text_fontsize, color='black')
                             .set_duration(answer_timestamp[1] - answer_timestamp[0])
                             .set_position('center')
                             .set_start(answer_timestamp[0])
                             .set_end(answer_timestamp[1]))

        segments.extend([flag_clip, answer_clip_white, answer_clip_black])

    # Composite all segments
    final_clip = CompositeVideoClip(segments, size=template_clip.size)

    # Export the final video
    output_filename = os.path.join(output_path, f"VID{video_id}.mp4")
    final_clip.write_videofile(output_filename, codec="libx264")

# Function to get the next available video ID
def get_next_video_id(output_path):
    existing_videos = [file for file in os.listdir(output_path) if file.startswith('VID') and file.endswith('.mp4')]
    if not existing_videos:
        return 1
    existing_ids = [int(file[3:-4]) for file in existing_videos]
    return max(existing_ids) + 1

# Number of videos 
num_videos = 5

# Get the next available video ID
next_video_id = get_next_video_id(output_path)

# Generate parameters for each video
params = [(random.choice(template_files), i, 170) for i in range(next_video_id, next_video_id + num_videos)]

# Set the number of processes to run in parallel (fixed number)
num_processes = num_videos  # Change this number to the desired number of parallel processes

# Run the video generation in parallel
if __name__ == '__main__':
    with Pool(num_processes) as pool:
        pool.map(create_video, params)
