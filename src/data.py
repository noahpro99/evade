import csv
from pathlib import Path

import requests
import urllib3

# Disable SSL warnings when we use verify=False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

OFFENDER_CSV_PATH = Path("data/offender_list - offender_list.csv")
OFFENDER_IMAGES_DIR = Path("data/offender_list/images")


def make_safe_name(name: str) -> str:
    """Convert a name to a filesystem-safe string."""
    safe = "".join(c for c in name if c.isalnum() or c in (" ", "-", "_")).rstrip()
    return safe.replace(" ", "_")


def unmake_safe_name(safe_name: str) -> str:
    """Convert a filesystem-safe string back to a regular name."""
    # remove extension if present
    if "." in safe_name:
        safe_name = safe_name.rsplit(".", 1)[0]
    return safe_name.replace("_", " ")

def get_image_path(name: str) -> Path:
    """Get the local image path for a given offender name."""
    safe_name = make_safe_name(name)
    return OFFENDER_IMAGES_DIR / f"{safe_name}.jpg"

def download_images_if_missing():
    OFFENDER_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    if OFFENDER_CSV_PATH.exists():
        with open(OFFENDER_CSV_PATH, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)  # Skip header row
            for row in reader:
                if len(row) > 1:  # Make sure there's a second column
                    name = row[0].strip()  # Name is in the first column (index 0)
                    link = row[1].strip()  # Image URL is in the second column (index 1)
                    if (
                        link and link.startswith("http") and name
                    ):  # Only add valid URLs with names
                        # Clean the name to be filesystem-safe
                        safe_name = make_safe_name(name)

                        # Use the person's name as the filename with .jpg extension
                        filename = OFFENDER_IMAGES_DIR / f"{safe_name}.jpg"
                        if not filename.exists():
                            try:
                                # Try with SSL verification first
                                try:
                                    resp = requests.get(link, timeout=10, verify=True)
                                except requests.exceptions.SSLError:
                                    # If SSL verification fails, try without verification
                                    print(
                                        f"SSL verification failed for {link}, trying without verification..."
                                    )
                                    resp = requests.get(link, timeout=10, verify=False)

                                if resp.status_code == 200:
                                    with open(filename, "wb") as f:
                                        f.write(resp.content)
                                    print(f"Downloaded {filename}")
                                else:
                                    print(
                                        f"Failed to download {link}: status {resp.status_code}"
                                    )
                            except Exception as e:
                                print(f"Error downloading {link}: {e}")
                        else:
                            print(f"Already exists: {filename}")


if __name__ == "__main__":
    download_images_if_missing()
