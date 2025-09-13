import os
import requests
from urllib.parse import urlparse
import uuid

def fetch_image():
    # Prompt user for the image URL
    url = input("Enter the image URL: ").strip()

    # Validate the URL
    if not url.startswith(('http://', 'https://')):
        print("❌ Error: Please enter a valid HTTP or HTTPS URL.")
        return

    # Create 'Fetched_Images' directory if it doesn't exist
    save_dir = "Fetched_Images"
    os.makedirs(save_dir, exist_ok=True)

    try:
        # Send GET request
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise error for bad responses (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching the image: {e}")
        return

    # Extract filename from URL
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)

    # If no filename found, generate one
    if not filename or '.' not in filename:
        filename = f'image_{uuid.uuid4().hex[:8]}.jpg'  # Default to jpg

    file_path = os.path.join(save_dir, filename)

    try:
        # Save image in binary mode
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"✅ Image saved successfully as: {file_path}")
    except IOError as e:
        print(f"❌ Error saving the image: {e}")

if __name__ == "__main__":
    fetch_image()
