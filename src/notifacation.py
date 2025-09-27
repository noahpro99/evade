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

def send_photo_dm(photo_url, recipient_username, message="Check out this photo!"):
    """
    Download a photo from URL and send it via Instagram DM with an optional message

    Args:
        photo_url (str): URL of the photo to download and send
        recipient_username (str): Instagram username of the recipient
        message (str): Optional message to send with the photo

    Returns:
        bool: True if successful, False if failed
    """
    try:
        # Create a temporary filename based on the URL
        photo_filename = Path(photo_url).name.split('?')[0]  # Remove query parameters
        if not photo_filename or '.' not in photo_filename:
            photo_filename = "temp_photo.jpg"
        photo_path = Path(f"temp_{photo_filename}")

        with open(photo_path, "wb") as f:
            f.write(response.content)
        print(f"Photo downloaded successfully: {photo_path}")

        # Get user ID
        user_id = cl.user_id_from_username(recipient_username)
        print(f"Sending photo to user ID: {user_id}")

        # Send photo first
        result = cl.direct_send_photo(str(photo_path), [user_id])
        print("Photo sent successfully!")

        # Send text message separately if provided
        if message:
            cl.direct_send(message, [user_id])
            print("Message sent successfully!")

        # Clean up temporary file
        if photo_path.exists():
            photo_path.unlink()
            print(f"Cleaned up temporary file: {photo_path}")

        return True

    except Exception as e:
        print(f"Failed to send photo/message: {e}")
        print(f"Error type: {type(e).__name__}")
        # Clean up on error too
        if 'photo_path' in locals() and photo_path.exists():
            photo_path.unlink()
        return False

def get_person_info(name):
    """Get information for a specific person from the CSV file"""
    csv_path = Path("data/offender_list - offender_list.csv")
    if csv_path.exists():
        with open(csv_path, "r", newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)  # Get header row
            for row in reader:
                if len(row) > 0 and row[0].strip().upper() == name.upper():
                    # Create a dictionary mapping headers to values
                    person_data = {}
                    for i, header in enumerate(headers):
                        if i < len(row):
                            person_data[header] = row[i]
                    return person_data
    return None

def send_offender_photo_dm(offender_name, recipient_username):
    """
    Send an offender's photo and information via Instagram DM

    Args:
        offender_name (str): Name of the offender from the CSV
        recipient_username (str): Instagram username of the recipient

    Returns:
        bool: True if successful, False if failed
    """
    try:
        # Get offender info from CSV
        offender_info = get_person_info(offender_name)
        if not offender_info:
            print(f"Offender '{offender_name}' not found in database")
            return False

        # Get photo URL from offender data (second column)
        photo_url = offender_info.get('', '').strip()  # Empty string key for the photo URL column
        if not photo_url or not photo_url.startswith('http'):
            print(f"No valid photo URL found for {offender_name}")
            return False

        # Create detailed message with offender info
        message = f"""🚨 OFFENDER ALERT 🚨

Name: {offender_info.get('Name', 'N/A')}
Age: {offender_info.get('Age', 'N/A')}
Status: {offender_info.get('Status', 'N/A')}
Tier: {offender_info.get('Tier', 'N/A')}
Height: {offender_info.get('Height', 'N/A')}
Weight: {offender_info.get('Weight', 'N/A')}
Hair: {offender_info.get('Hair', 'N/A')}
Eyes: {offender_info.get('Eyes', 'N/A')}
Race: {offender_info.get('Race', 'N/A')}

Registration #: {offender_info.get('Probation Registration Number', 'N/A')}
Convictions: {offender_info.get('Convictions', 'N/A')}

⚠️ Stay alert and report any sightings to authorities."""

        # Send photo and message
        return send_photo_dm(photo_url, recipient_username, message)

    except Exception as e:
        print(f"Failed to send offender alert: {e}")
        return False

if __name__ == "__main__":
    # Example usage - send Noah's photo and info
    success = send_offender_photo_dm("NOAH PROVENZANO", "sethpro9")
    if success:
        print("Offender alert sent successfully!")
    else:
        print("Failed to send offender alert.")

    # Alternative: send any photo URL
    # photo_url = "https://example.com/photo.jpg"
    # success = send_photo_dm(photo_url, "recipient_username", "Custom message")
    # if success:
    #     print("Photo sent successfully!")
    # else:
    #     print("Failed to send photo.")