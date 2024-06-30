import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from datetime import datetime, timedelta

# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

# Authenticate with OAuth2
def authenticate_with_oauth(client_secrets_file):
    flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
    credentials = flow.run_local_server(port=0)
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
        "contentDetails": {
            "selfDeclaredMadeForKids": False  # Set to False for "No, It's not made for kids"
        }
    }

    media = MediaFileUpload(file, chunksize=-1, resumable=True)
    
    request = youtube.videos().insert(
        part="snippet,status,contentDetails",  # Include contentDetails in the part parameter
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print("Uploaded {0}%.".format(int(status.progress() * 100)))
    print("Upload Complete!")
    return response

# Paths and variables
client_secrets_file = r'C:\Users\panjw_gco4a0t\Documents\GitHub\VideoAutomater\automate upload HALFWORKING]\client_secret_100613254388-kutfqde516r1agg6iqnl161c0id4ls90.apps.googleusercontent.com (2).json'  # Update with your JSON file path
video_directory = r'C:\Users\panjw_gco4a0t\Documents\GitHub\VideoAutomater\OUTPUT'  # Directory containing videos to upload

# Authenticate
youtube = authenticate_with_oauth(client_secrets_file)

# Set the initial publish time (8 PM on June 30th, 2024)
initial_publish_time = datetime(2024, 6, 30, 3, 0, 0)  # Adjusted for MST

# Get list of all video files in the directory
for i, filename in enumerate(os.listdir(video_directory)):
    if filename.endswith(".mp4"):
        file_path = os.path.join(video_directory, filename)
        
        # Customize video details
        video_title = f"WHATS YOUR GEOGRAPHY LEVEL 💯💯🔴👇"
        video_description = f"😎👍#flag #geography #geographyquiz #quiz #foryou #trending #easy #maps"
        video_tags = ["geography", "geoquiz", "quiz", "country", "map", "geographyquiz", "easy", "foryou", "trending", "flag", "shorts"]
        video_category = "22"  # People & Blogs
        privacy_status = "private"  
        
        # Calculate publish time for this video
        publish_at = (initial_publish_time + timedelta(minutes=30 * i)).isoformat("T") + "Z"
        
        # Upload video
        upload_video(youtube, file_path, video_title, video_description, category=video_category, tags=video_tags, privacy_status=privacy_status, publish_at=publish_at)
        
        # Delete the file after successful upload
        os.remove(file_path)
        print(f"Deleted {file_path} after upload.")
