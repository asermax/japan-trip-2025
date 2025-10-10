#!/usr/bin/env python3
"""Quick broken image finder for Japan Trip 2025 attractions, destinations, and routes.

Usage examples:
  python find_broken_images.py                       # Check all files
  python find_broken_images.py osaka                 # Check specific destination
  python find_broken_images.py kinosaki-to-itoshima  # Check specific route pair
"""

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
    parser.add_argument('target', nargs='?', help='Specific destination or route pair (e.g., kinosaki-to-itoshima) (optional)')
    args = parser.parse_args()

    attractions_dir = Path('research/attractions')
    destinations_dir = Path('research/destinations')
    routes_dir = Path('research/routes')

    if args.target and '-to-' in args.target:
        # Check specific route pair (e.g., kinosaki-to-itoshima)
        # Find all route folders matching this pattern
        route_folders = [d for d in routes_dir.iterdir() if d.is_dir() and d.name.startswith(args.target)]
        attraction_folders = [d for d in attractions_dir.iterdir() if d.is_dir() and d.name.startswith(args.target)]

        route_files = []
        for folder in route_folders:
            route_files.extend(list(folder.glob('*.md')))

        route_attraction_files = []
        for folder in attraction_folders:
            route_attraction_files.extend(list(folder.glob('*.md')))

        all_files = route_files + route_attraction_files
        print(f"Checking {args.target} routes...")
        print(f"Found {len(route_folders)} route folders with {len(route_files)} route files")
        print(f"Found {len(attraction_folders)} attraction folders with {len(route_attraction_files)} route attraction files")
    elif args.target:
        # Check specific destination
        attraction_files = list((attractions_dir / args.target).glob('*.md')) if (attractions_dir / args.target).exists() else []
        destination_file = destinations_dir / f'{args.target}.md'
        destination_files = [destination_file] if destination_file.exists() else []
        all_files = attraction_files + destination_files
        print(f"Checking {args.target}...")
        print(f"Found {len(attraction_files)} attraction files and {len(destination_files)} destination files")
    else:
        # Check all files (destinations, attractions, and routes)
        attraction_files = list(attractions_dir.rglob('*.md'))
        destination_files = list(destinations_dir.rglob('*.md'))
        route_files = list(routes_dir.rglob('*.md'))
        all_files = attraction_files + destination_files + route_files
        print(f"Checking all files...")
        print(f"Found {len(attraction_files)} attraction files, {len(destination_files)} destination files, and {len(route_files)} route files")

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