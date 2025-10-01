#!/usr/bin/env -S uv run python
"""
Add GPS coordinates to attraction files that are missing them.
Uses Google Geocoding API to look up coordinates based on location text.
Requires: .env file with GOOGLE_MAPS_API_KEY
"""

import re
import time
import os
from pathlib import Path
from typing import Optional, Tuple
import urllib.parse
import urllib.request
import json

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Get API key from environment
GOOGLE_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')
if not GOOGLE_API_KEY:
    print("❌ Error: GOOGLE_MAPS_API_KEY not found in .env file")
    exit(1)


def extract_location_text(content: str) -> Optional[str]:
    """Extract the location description from the file."""
    # Look for **Location:** line that doesn't have a Google Maps link
    match = re.search(r'\*\*Location:\*\*\s+([^\[]+?)(?:\n|$)', content)
    if match:
        return match.group(1).strip()
    return None


def has_coordinates(content: str) -> bool:
    """Check if file already has GPS coordinates."""
    return bool(re.search(r'maps\.google\.com/maps\?q=[-+]?\d+\.?\d*,[-+]?\d+\.?\d*', content))


def geocode_location(location_text: str) -> Optional[Tuple[float, float]]:
    """Use Google Geocoding API to get coordinates for a location."""
    # Add Japan to the query to improve accuracy
    query = f"{location_text}, Japan"
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={urllib.parse.quote(query)}&key={GOOGLE_API_KEY}"
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            
        if data['status'] == 'OK' and len(data['results']) > 0:
            location = data['results'][0]['geometry']['location']
            return (location['lat'], location['lng'])
        else:
            print(f"  ⚠️  Geocoding failed: {data.get('status', 'UNKNOWN')}")
            return None
            
    except Exception as e:
        print(f"  ❌ Error geocoding: {e}")
        return None


def add_coordinates_to_file(file_path: Path, dry_run: bool = False) -> bool:
    """Add coordinates to a single file."""
    content = file_path.read_text()
    
    if has_coordinates(content):
        return False  # Already has coordinates
    
    location_text = extract_location_text(content)
    if not location_text:
        print(f"  ⚠️  No location text found in {file_path.name}")
        return False
    
    print(f"  📍 Looking up: {location_text}")
    coords = geocode_location(location_text)
    
    if not coords:
        return False
    
    lat, lng = coords
    maps_url = f"https://maps.google.com/maps?q={lat},{lng}"
    
    # Find the Location line and add coordinates after it
    location_pattern = r'(\*\*Location:\*\*\s+[^\[]+?)(\n)'
    replacement = f'\\1\\2**Location:** [View on Google Maps]({maps_url})\\2'
    
    new_content = re.sub(location_pattern, replacement, content, count=1)
    
    if new_content == content:
        print(f"  ⚠️  Could not insert coordinates into {file_path.name}")
        return False
    
    if not dry_run:
        file_path.write_text(new_content)
        print(f"  ✅ Added coordinates: {lat}, {lng}")
    else:
        print(f"  ✅ Would add coordinates: {lat}, {lng}")
    
    return True


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Add GPS coordinates to attraction files')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    parser.add_argument('--limit', type=int, help='Limit number of files to process')
    parser.add_argument('path', nargs='?', default='research/attractions', help='Path to attractions directory')
    
    args = parser.parse_args()
    
    attractions_path = Path(args.path)
    if not attractions_path.exists():
        print(f"❌ Path not found: {attractions_path}")
        return
    
    # Find all markdown files
    files = list(attractions_path.rglob("*.md"))
    
    # Filter to only files missing coordinates
    files_to_process = []
    for file in files:
        content = file.read_text()
        if not has_coordinates(content):
            files_to_process.append(file)
    
    if args.limit:
        files_to_process = files_to_process[:args.limit]
    
    print(f"🔍 Found {len(files_to_process)} attraction files missing coordinates")
    
    if args.dry_run:
        print("🔬 DRY RUN MODE - No files will be modified\n")
    
    processed = 0
    failed = 0
    
    for i, file in enumerate(files_to_process, 1):
        print(f"\n[{i}/{len(files_to_process)}] Processing {file.relative_to(attractions_path)}")
        
        try:
            if add_coordinates_to_file(file, dry_run=args.dry_run):
                processed += 1
                # Rate limit to avoid hitting API limits
                time.sleep(0.2)
            else:
                failed += 1
        except Exception as e:
            print(f"  ❌ Error: {e}")
            failed += 1
    
    print(f"\n{'🔬 DRY RUN ' if args.dry_run else ''}Summary:")
    print(f"  ✅ Processed: {processed}")
    print(f"  ❌ Failed: {failed}")
    print(f"  📊 Total: {len(files_to_process)}")


if __name__ == '__main__':
    main()
