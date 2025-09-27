import csv
from pathlib import Path
import requests

OFFENDER_CSV = Path("data/offender_list - offender_list.csv")


def download_images_if_missing():
    images_dir = Path("data/offender_list/images")
    images_dir.mkdir(parents=True, exist_ok=True)

    if OFFENDER_CSV.exists():
        with open(OFFENDER_CSV, "r", newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header row
            for row in reader:
                if len(row) > 1:  # Make sure there's a second column
                    name = row[0].strip()  # Name is in the first column (index 0)
                    link = row[1].strip()  # Image URL is in the second column (index 1)
                    if link and link.startswith('http') and name:  # Only add valid URLs with names
                        # Clean the name to be filesystem-safe
                        safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).rstrip()
                        safe_name = safe_name.replace(' ', '_')
                        
                        # Use the person's name as the filename with .jpg extension
                        filename = images_dir / f"{safe_name}.jpg"
                        if not filename.exists():
                            try:
                                resp = requests.get(link, timeout=10)
                                if resp.status_code == 200:
                                    with open(filename, "wb") as f:
                                        f.write(resp.content)
                                    print(f"Downloaded {filename}")
                                else:
                                    print(f"Failed to download {link}: status {resp.status_code}")
                            except Exception as e:
                                print(f"Error downloading {link}: {e}")
                        else:
                            print(f"Already exists: {filename}")