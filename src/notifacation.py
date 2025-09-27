from instagrapi import Client
from pathlib import Path
import csv
import requests
from settings import settings

# Initialize the client
cl = Client()

# Login with your Instagram credentials
username = settings.INSTAGRAM_USERNAME
password = settings.INSTAGRAM_PASSWORD

try:
    cl.login(username, password)
    print("Login successful!")
except Exception as e:
    print(f"Login failed: {e}")
    exit(1)

# Photo details
photo_url = "https://media.licdn.com/dms/image/v2/D4E03AQGTDul6VG4aLg/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1726866822502?e=1761782400&v=beta&t=bzu2q7kJsXbF0IavRHHsQBPlyEqrevwBWGV1XzhQJ6M"
photo_path = Path("downloaded_photo.jpg")

# Download the photo
try:
    response = requests.get(photo_url)
    response.raise_for_status()  # Check for HTTP errors
    with open(photo_path, "wb") as f:
        f.write(response.content)
    print(f"Photo downloaded successfully: {photo_path}")
except Exception as e:
    print(f"Failed to download photo: {e}")
    exit(1)

# Send the photo as a direct message
try:
    recipient_username = "sethpro9"  # Replace with the recipient's username
    user_id = cl.user_id_from_username(recipient_username)
    print(f"Sending photo to user ID: {user_id}")

    # Send photo first (current API doesn't support text parameter)
    result = cl.direct_send_photo(str(photo_path), [user_id])
    print("Photo sent successfully!")

    # Send text message separately
    message = "Check out this photo!"
    cl.direct_send(message, [user_id])
    print("Message sent successfully!")

except Exception as e:
    print(f"Failed to send photo/message: {e}")
    print(f"Error type: {type(e).__name__}")