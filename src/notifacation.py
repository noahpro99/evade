from pathlib import Path

from instagrapi import Client

from settings import settings

instagram_client = Client()

try:
    instagram_client.login(settings.INSTAGRAM_USERNAME, settings.INSTAGRAM_PASSWORD)
    print("Login successful!")
except Exception as e:
    print(f"Login failed: {e}")
    exit(1)


def send_photo_dm(photo_path, recipient_username, message="Check out this photo!"):
    """
    Send a local photo via Instagram DM with an optional message

    Args:
        photo_path (str or Path): Path to the local photo file to send
        recipient_username (str): Instagram username of the recipient
        message (str): Optional message to send with the photo

    Returns:
        bool: True if successful, False if failed
    """
    try:
        # Convert to Path object and check if file exists
        photo_file = Path(photo_path)
        if not photo_file.exists():
            print(f"Photo file not found: {photo_file}")
            return False

        print(f"Sending photo: {photo_file}")

        user_id = int(instagram_client.user_id_from_username(recipient_username))
        print(f"Sending photo to user ID: {user_id}")

        # Send photo first
        result = instagram_client.direct_send_photo(photo_file, [user_id])
        print(f"Photo sent successfully! Result: {result}")

        # Send text message separately if provided
        if message:
            instagram_client.direct_send(message, [user_id])
            print("Message sent successfully!")

        return True

    except Exception as e:
        print(f"Failed to send photo DM: {e}")
        print(f"Error type: {type(e).__name__}")
        return False


def send_text_dm(recipient_username, message):
    """
    Send a text message via Instagram DM

    Args:
        recipient_username (str): Instagram username of the recipient
        message (str): Message to send

    Returns:
        bool: True if successful, False if failed
    """
    try:
        user_id = int(instagram_client.user_id_from_username(recipient_username))
        print(f"Sending text message to user ID: {user_id}")

        result = instagram_client.direct_send(message, [user_id])
        print(f"Text message sent successfully! Result: {result}")

        return True

    except Exception as e:
        print(f"Failed to send text message: {e}")
        print(f"Error type: {type(e).__name__}")
        return False
