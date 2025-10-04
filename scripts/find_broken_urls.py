#!/usr/bin/env python3
"""Quick broken URL finder for Japan Trip 2025 research files."""

import argparse
import os
import re
import requests
from pathlib import Path


def extract_urls_from_file(file_path):
    """Extract all URLs from a markdown file (links and source citations)."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match markdown links: [text](url)
    markdown_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)

    # Match source citations: [🔗](url) or similar emoji links
    source_citations = re.findall(r'\[[\u2000-\u3300]\]\(([^)]+)\)', content)

    urls = []

    # Process markdown links
    for link_text, url in markdown_links:
        # Skip internal links (starting with /)
        if url.startswith('/'):
            continue

        # Skip anchor links
        if url.startswith('#'):
            continue

        # Skip email links
        if url.startswith('mailto:'):
            continue

        urls.append({
            'file': str(file_path),
            'text': link_text,
            'url': url,
            'type': 'link'
        })

    # Process source citations
    for url in source_citations:
        if not url.startswith('/') and not url.startswith('#'):
            urls.append({
                'file': str(file_path),
                'text': '🔗 Source Citation',
                'url': url,
                'type': 'citation'
            })

    return urls


def is_broken_url(url):
    """Quick check if URL is broken."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.head(url, headers=headers, timeout=10, allow_redirects=True)

        if response.status_code >= 400:
            return True, f"HTTP {response.status_code}"

        return False, "OK"
    except requests.exceptions.Timeout:
        return True, "Timeout"
    except requests.exceptions.TooManyRedirects:
        return True, "Too many redirects"
    except requests.exceptions.SSLError:
        return True, "SSL Error"
    except requests.exceptions.ConnectionError as e:
        return True, f"Connection error: {str(e)[:50]}"
    except Exception as e:
        return True, str(e)[:50]


def main():
    parser = argparse.ArgumentParser(description='Find broken URLs in research files')
    parser.add_argument('destination', nargs='?', help='Specific destination to check (optional)')
    parser.add_argument('--routes', action='store_true', help='Check route files instead of attractions')
    parser.add_argument('--offset', type=int, default=0, help='Skip first N files')
    parser.add_argument('--limit', type=int, help='Process only N files after offset')
    args = parser.parse_args()

    if args.routes:
        # Check routes
        routes_dir = Path('research/routes')
        if args.destination:
            # Check specific route folder
            route_folders = [d for d in routes_dir.iterdir() if d.is_dir() and args.destination in d.name]
            all_files = []
            for folder in route_folders:
                all_files.extend(folder.rglob('*.md'))
            print(f"Checking routes matching '{args.destination}'...")
        else:
            # Check all route files
            all_files = list(routes_dir.rglob('*.md'))
            print(f"Checking all route files...")
    else:
        # Check attractions and destinations
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
            print(f"Checking all attraction and destination files...")

        all_files = attraction_files + destination_files

    total_files = len(all_files)
    print(f"Found {total_files} files total")

    # Apply offset and limit
    if args.offset > 0:
        all_files = all_files[args.offset:]
        print(f"Skipping first {args.offset} files")

    if args.limit:
        all_files = all_files[:args.limit]
        print(f"Processing {len(all_files)} files (offset: {args.offset}, limit: {args.limit})")
    else:
        print(f"Processing {len(all_files)} files")

    all_urls = []
    for file_path in all_files:
        urls = extract_urls_from_file(file_path)
        all_urls.extend(urls)

    print(f"Found {len(all_urls)} URLs to validate\n")

    broken_urls = []
    for i, url_info in enumerate(all_urls, 1):
        print(f"[{i}/{len(all_urls)}] {Path(url_info['file']).name} - {url_info['text'][:30]}...", end=' ')

        is_broken, error = is_broken_url(url_info['url'])
        if is_broken:
            print(f"❌ {error}")
            broken_urls.append({**url_info, 'error': error})
        else:
            print("✅")

    print(f"\n{'='*80}")
    print(f"BROKEN URLs SUMMARY ({len(broken_urls)} found):")
    print(f"{'='*80}")

    # Group by file for better readability
    from collections import defaultdict
    by_file = defaultdict(list)
    for broken in broken_urls:
        by_file[broken['file']].append(broken)

    for file_path, urls in sorted(by_file.items()):
        print(f"\n📄 File: {Path(file_path).relative_to('research')}")
        for i, url_info in enumerate(urls, 1):
            print(f"  {i}. [{url_info['type']}] {url_info['text'][:50]}")
            print(f"     URL: {url_info['url']}")
            print(f"     Error: {url_info['error']}")

    return broken_urls


if __name__ == "__main__":
    broken = main()
    print(f"\n{'='*80}")
    print(f"Found {len(broken)} broken URLs to fix.")
    print(f"{'='*80}")
