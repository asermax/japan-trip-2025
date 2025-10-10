#!/usr/bin/env python3
"""
Find orphaned attractions - attractions that exist in research/attractions/{route-name}/
but are not properly referenced in the corresponding route markdown file.

Outputs JSON with route information and orphaned attractions for parallel agent processing.
"""

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Set


def extract_route_sections(content: str) -> Dict[str, Set[str]]:
    """
    Extract attractions mentioned in each section of the route file.
    Returns a dict mapping section keys to sets of attraction slugs.
    """
    sections = {
        'on_route': set(),
        'short_detour': set(),
        'major_detour': set()
    }

    # Find section boundaries
    section_patterns = [
        (r'## On-Route Stops', 'on_route'),
        (r'## Short Detour Stops', 'short_detour'),
        (r'## Major Detour Stops', 'major_detour')
    ]

    lines = content.split('\n')
    current_section = None

    for i, line in enumerate(lines):
        # Check if we're entering a new section
        for pattern, section_key in section_patterns:
            if re.match(pattern, line):
                current_section = section_key
                break

        # Check if we're leaving a section (next ## heading)
        if current_section and line.startswith('## ') and not any(
            re.match(pattern, line) for pattern, _ in section_patterns
        ):
            current_section = None

        # Extract attraction references in current section
        if current_section:
            # Look for research file references
            match = re.search(r'research/attractions/[^/]+/([^/\]]+)\.md', line)
            if match:
                sections[current_section].add(match.group(1))

            # Also look for ### headings as potential attractions
            if line.startswith('### '):
                # Convert title to slug format (lowercase, spaces to hyphens)
                title = line[4:].strip()
                slug = title.lower().replace(' ', '-').replace('(', '').replace(')', '')
                sections[current_section].add(slug)

    return sections


def find_orphaned_for_route(route_name: str, research_dir: Path) -> Dict:
    """
    Find orphaned attractions for a single route.
    Returns dict with route info and orphaned attractions by section.
    """
    # Find the route markdown file
    route_dir = research_dir / "routes" / route_name
    route_files = list(route_dir.glob("*.md"))

    if not route_files:
        return {
            'route_name': route_name,
            'error': f"No route file found in {route_dir}"
        }

    route_file = route_files[0]
    attractions_dir = research_dir / "attractions" / route_name

    if not attractions_dir.exists():
        return {
            'route_name': route_name,
            'error': f"Attractions directory not found: {attractions_dir}"
        }

    # Get all attraction files
    attraction_files = list(attractions_dir.glob("*.md"))
    all_attraction_slugs = {f.stem for f in attraction_files}

    # Read route file and extract referenced attractions
    with open(route_file, 'r', encoding='utf-8') as f:
        content = f.read()

    referenced_sections = extract_route_sections(content)

    # Combine all referenced attractions
    all_referenced = set()
    for attractions in referenced_sections.values():
        all_referenced.update(attractions)

    # Find orphaned attractions
    orphaned_slugs = all_attraction_slugs - all_referenced

    if not orphaned_slugs:
        return {
            'route_name': route_name,
            'route_file': str(route_file),
            'total_attractions': len(all_attraction_slugs),
            'orphaned_count': 0,
            'orphaned': {}
        }

    # Categorize orphaned attractions by reading their files
    orphaned_by_section = {
        'on_route': [],
        'short_detour': [],
        'major_detour': []
    }

    for slug in orphaned_slugs:
        attraction_file = attractions_dir / f"{slug}.md"

        # Read attraction file to determine category
        with open(attraction_file, 'r', encoding='utf-8') as f:
            attraction_content = f.read()
            # Extract title from first line of content
            first_line = attraction_content.split('\n')[0].strip()
            title = first_line[2:] if first_line.startswith('# ') else first_line

        # Determine category based on content hints
        # Look for detour time mentions or category indicators
        category = 'major_detour'  # Default to major detour

        if 'no detour' in attraction_content.lower() or 'on-route' in attraction_content.lower():
            category = 'on_route'
        elif '15-30 min' in attraction_content or 'short detour' in attraction_content.lower():
            category = 'short_detour'
        elif 'detour time:**' in attraction_content.lower():
            # Extract detour time if specified
            detour_match = re.search(r'\*\*Detour Time:\*\*\s*([^*\n]+)', attraction_content, re.IGNORECASE)
            if detour_match:
                detour_text = detour_match.group(1).lower()
                if 'no detour' in detour_text or 'on route' in detour_text:
                    category = 'on_route'
                elif any(x in detour_text for x in ['15 min', '20 min', '25 min', '30 min']):
                    category = 'short_detour'

        orphaned_by_section[category].append({
            'slug': slug,
            'title': title,
            'file': str(attraction_file)
        })

    return {
        'route_name': route_name,
        'route_file': str(route_file),
        'total_attractions': len(all_attraction_slugs),
        'orphaned_count': len(orphaned_slugs),
        'orphaned': orphaned_by_section
    }


def main():
    parser = argparse.ArgumentParser(
        description="Find orphaned attractions in route files"
    )
    parser.add_argument(
        "--research",
        type=Path,
        default=Path("research"),
        help="Path to research directory"
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output JSON file path (default: stdout)"
    )

    args = parser.parse_args()

    # Find all route directories
    routes_dir = args.research / "routes"
    route_dirs = [d for d in routes_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]

    results = []

    for route_dir in sorted(route_dirs):
        route_name = route_dir.name
        result = find_orphaned_for_route(route_name, args.research)
        results.append(result)

    # Filter to only routes with orphaned attractions
    orphaned_routes = [r for r in results if r.get('orphaned_count', 0) > 0]

    output = {
        'total_routes': len(results),
        'routes_with_orphans': len(orphaned_routes),
        'total_orphaned': sum(r.get('orphaned_count', 0) for r in results),
        'routes': orphaned_routes
    }

    # Output JSON
    json_output = json.dumps(output, indent=2)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(json_output)
        print(f"✅ Results written to {args.output}")
    else:
        print(json_output)


if __name__ == "__main__":
    main()
