#!/usr/bin/env python3
"""Quick broken image finder for Japan Trip 2025 attractions."""

import argparse
import os
import re
import requests
from pathlib import Path

def extract_image_urls_from_file(file_path):
    """Extract image URLs from a markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    matches = re.findall(pattern, content)

    images = []
    for alt_text, url in matches:
        images.append({
            'file': str(file_path),
            'alt': alt_text,
            'url': url
        })
    return images

def is_broken_image(url):
    """Quick check if image URL is broken."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.head(url, headers=headers, timeout=5, allow_redirects=True)

        if response.status_code != 200:
            return True, f"HTTP {response.status_code}"

        content_type = response.headers.get('content-type', '').lower()
        if not any(img_type in content_type for img_type in ['image/', 'jpeg', 'jpg', 'png', 'gif', 'webp']):
            return True, f"Invalid content type: {content_type}"

        return False, "OK"
    except Exception as e:
        return True, str(e)

def main():
    parser = argparse.ArgumentParser(description='Find broken images in research files')
    parser.add_argument('destination', nargs='?', help='Specific destination to check (optional)')
    args = parser.parse_args()

    attractions_dir = Path('research/attractions')
    destinations_dir = Path('research/destinations')

    if args.destination:
        # Check specific destination
        attraction_files = list((attractions_dir / args.destination).glob('*.md')) if (attractions_dir / args.destination).exists() else []
        destination_file = destinations_dir / f'{args.destination}.md'
        destination_files = [destination_file] if destination_file.exists() else []
        print(f"Checking {args.destination}...")
    else:
        # Check all files
        attraction_files = list(attractions_dir.rglob('*.md'))
        destination_files = list(destinations_dir.rglob('*.md'))
        print(f"Checking all files...")

    all_files = attraction_files + destination_files
    print(f"Found {len(attraction_files)} attraction files and {len(destination_files)} destination files")

    all_images = []
    for file_path in all_files:
        images = extract_image_urls_from_file(file_path)
        all_images.extend(images)

    print(f"Found {len(all_images)} images to validate\n")

    broken_images = []
    for i, img in enumerate(all_images, 1):
        print(f"[{i}/{len(all_images)}] {Path(img['file']).name}...", end=' ')

        is_broken, error = is_broken_image(img['url'])
        if is_broken:
            print(f"❌ {error}")
            broken_images.append({**img, 'error': error})
        else:
            print("✅")

    print(f"\n{'='*50}")
    print(f"BROKEN IMAGES SUMMARY ({len(broken_images)} found):")
    print(f"{'='*50}")

    for broken in broken_images:
        print(f"\nFile: {Path(broken['file']).name}")
        print(f"Alt: {broken['alt']}")
        print(f"URL: {broken['url']}")
        print(f"Error: {broken['error']}")

    return broken_images

if __name__ == "__main__":
    broken = main()
    print(f"\nFound {len(broken)} broken images to fix.")