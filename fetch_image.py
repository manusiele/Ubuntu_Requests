import requests
import os
import hashlib
from urllib.parse import urlparse

def get_filename_from_url(url):
    parsed = urlparse(url)
    filename = os.path.basename(parsed.path)
    if not filename or '.' not in filename:
        filename = "image_" + hashlib.md5(url.encode()).hexdigest()[:8] + ".jpg"
    return filename

def is_image(content_type):
    return content_type.startswith("image/")

def already_downloaded(filepath, new_content):
    if not os.path.exists(filepath):
        return False
    with open(filepath, 'rb') as f:
        existing_content = f.read()
    return existing_content == new_content

def fetch_and_save_image(url, save_dir):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        content_type = response.headers.get("Content-Type", "")
        if not is_image(content_type):
            print(f"✗ Skipped: {url} is not an image (Content-Type: {content_type})")
            return

        filename = get_filename_from_url(url)
        filepath = os.path.join(save_dir, filename)

        if already_downloaded(filepath, response.content):
            print(f"• Duplicate skipped: {filename} already exists with same content.")
            return
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error for {url}: {e}")
    except Exception as e:
        print(f"✗ An error occurred for {url}: {e}")

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    # Input: multiple URLs separated by spaces or commas
    raw_input = input("Please enter one or more image URLs (separated by spaces or commas):\n")
    urls = [url.strip() for url in raw_input.replace(',', ' ').split()]
    
    if not urls:
        print("✗ No valid URLs provided.")
        return
    
    # Create directory if it doesn't exist
    save_dir = "Fetched_Images"
    os.makedirs(save_dir, exist_ok=True)
    
    for url in urls:
        fetch_and_save_image(url, save_dir)

    print("\nConnection strengthened. Community enriched.")

if __name__ == "__main__":
    main()
