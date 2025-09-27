from instagrapi import Client

# Initialize the client
cl = Client()

# Login with your Instagram credentials
username = ""
password = ""
verification_code = input("Enter the 2FA code sent to your device: ")
cl.login(username, password, verification_code=verification_code)

# Send a direct message
recipient_username = "noahpro99"
message_text = "1234!"

# Get user id of the recipient
user_id = cl.user_id_from_username(recipient_username)

# Send the message
cl.direct_send(message_text, [user_id])