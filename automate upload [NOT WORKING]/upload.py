import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from datetime import datetime, timedelta

# Path to the service account JSON key file
service_account_file = '/path/to/your/service_account_key.json'

# Define the scopes (if necessary)
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

# Authenticate with service account
def authenticate_with_service_account(credentials_file, scopes):
    credentials = service_account.Credentials.from_service_account_file(
        credentials_file, scopes=scopes)
    return build('youtube', 'v3', credentials=credentials)

# Function to upload video
def upload_video(youtube, file, title, description, category="22", tags=None, privacy_status="private", publish_at=None):
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": category
        },
        "status": {
            "privacyStatus": privacy_status,
            "publishAt": publish_at
        },
        "shortsVideoDuration": "SHORT"  # Specifies that the video is intended for YouTube Shorts
    }

    media = MediaFileUpload(file, chunksize=-1, resumable=True)
    
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None  # Initialize response variable
    
    while response is None:
        status, response = request.next_chunk()
        if status:
            print("Uploaded {0}%.".format(int(status.progress() * 100)))
    print("Upload Complete!")
    return response

# Paths and variables
video_directory = '/path/to/your/video/directory'

# Authenticate using service account
youtube = authenticate_with_service_account(service_account_file, SCOPES)

# Set the initial publish time (8 PM on June 30th, 2024)
initial_publish_time = datetime(2024, 6, 30, 20, 0, 0)  # YYYY, MM, DD, HH, MM, SS

# Get list of all video files in the directory
for i, filename in enumerate(os.listdir(video_directory)):
    if filename.endswith(".mp4"):
        file_path = os.path.join(video_directory, filename)
        
        # Customize video details for Shorts
        video_title = f"Shorts: {filename}"
        video_description = f"This video is a YouTube Shorts video titled {filename}. Enjoy watching!"
        video_tags = ["shorts", "video", "upload"]
        video_category = "22"  # People & Blogs
        privacy_status = "private"  # or "public", "unlisted"
        
        # Calculate publish time for this video
        publish_at = (initial_publish_time + timedelta(minutes=30 * i)).isoformat("T") + "Z"
        
        # Upload video as Shorts
        upload_video(youtube, file_path, video_title, video_description, category=video_category, tags=video_tags, privacy_status=privacy_status, publish_at=publish_at)
        
        # Delete the file after successful upload
        os.remove(file_path)
        print(f"Deleted {file_path} after upload.")
