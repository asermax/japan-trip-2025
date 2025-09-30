#!/usr/bin/env python3
"""
Generate timeline-based Zola content from research files.
This script reads structured research files and generates timeline entries, place guides, and attraction pages.
"""

import os
import sys
import re
import unicodedata
from pathlib import Path
from datetime import datetime, timedelta
import argparse
import markdown
from typing import Dict, List, Any, Optional

# Category mapping for organizing attractions
CATEGORY_GROUPS = {
    "Cultural & Historic Sites": ["museum", "heritage", "historic", "cultural", "folk", "government", "exhibition"],
    "Temples & Shrines": ["temple", "shrine", "buddhist", "shinto", "religious"],
    "Traditional Experiences": ["craft", "workshop", "brewery", "sake", "traditional", "lacquerware"],
    "Natural & Scenic": ["park", "mountain", "forest", "cave", "natural", "scenic", "viewpoint", "observation", "deck", "ropeway", "tramway"],
    "Culinary Experiences": ["restaurant", "cuisine", "dining", "coffee", "cafe", "food", "culinary", "cutlet", "beef", "premium"],
    "Entertainment & Modern": ["amusement", "music", "modern", "highland"],
    "Wellness & Relaxation": ["onsen", "hot spring", "spa", "relaxation"]
}

# Order for displaying categories
CATEGORY_ORDER = [
    "Cultural & Historic Sites",
    "Temples & Shrines",
    "Traditional Experiences",
    "Natural & Scenic",
    "Culinary Experiences",
    "Entertainment & Modern",
    "Wellness & Relaxation"
]

def create_url_slug(text: str) -> str:
    """Convert text to URL-friendly slug using Unicode normalization."""
    # Normalize Unicode characters (convert accented chars to base + combining chars)
    text = unicodedata.normalize('NFKD', text)

    # Encode to ASCII bytes, ignoring non-ASCII chars, then decode back to string
    text = text.encode('ascii', 'ignore').decode('ascii')

    # Convert to lowercase
    slug = text.lower()

    # Replace common special cases
    slug = slug.replace('&', 'and')  # Convert & to and
    slug = slug.replace('+', 'plus') # Convert + to plus
    slug = slug.replace('@', 'at')   # Convert @ to at

    # Replace spaces and other separators with hyphens
    slug = re.sub(r'[\s\-_\.]+', '-', slug)

    # Remove any characters that aren't letters, numbers, or hyphens
    slug = re.sub(r'[^a-z0-9\-]', '', slug)

    # Remove multiple consecutive hyphens
    slug = re.sub(r'-+', '-', slug)

    # Remove leading/trailing hyphens
    slug = slug.strip('-')

    return slug


def escape_toml_string(text: str) -> str:
    """Escape special characters for TOML basic strings."""
    if text is None:
        return ""
    # Escape backslashes first (must be first!)
    text = text.replace('\\', '\\\\')
    # Then escape double quotes
    text = text.replace('"', '\\"')
    # Escape control characters
    text = text.replace('\n', '\\n')
    text = text.replace('\r', '\\r')
    text = text.replace('\t', '\\t')
    return text


# Timeline entry template
TIMELINE_ENTRY_TEMPLATE = """+++
title = "{title}"
description = "{description}"
date = {date}
weight = {weight}
template = "timeline-entry.html"

[extra]
timeline_order = {order}
type = "{entry_type}"
date_range = "{date_range}"
duration = "{duration}"
{extra_fields}
+++

{content}

---

*Generated from research: {source_files}*
"""

# Attraction template
ATTRACTION_TEMPLATE = """+++
title = "{title}"
description = "{description}"
weight = {weight}
categories = {categories}
tags = {tags}
template = "attraction.html"

[extra]
location = "{location}"
category = "{category}"
cost = "{cost}"
best_time = "{best_time}"
place = "{place}"
timeline_entries = {timeline_entries}
difficulty = "{difficulty}"
duration = "{visit_duration}"
previous_attraction = "{previous_attraction}"
next_attraction = "{next_attraction}"
previous_title = "{previous_title}"
next_title = "{next_title}"
+++

{content}

*Source: {source_file}*
"""

class TimelineGenerator:
    def __init__(self, research_dir: Path, output_dir: Path):
        self.research_dir = Path(research_dir)
        self.output_dir = Path(output_dir)
        self.timeline_config = []
        self.routes_dir = self.research_dir / "routes"

    def parse_visit_date(self, visit_period: str) -> Optional[datetime]:
        """Parse visit period string into datetime object for sorting."""
        if not visit_period:
            return None

        # Handle formats like "October 23-24, 2025" or "Oct 23-24, 2025"
        month_map = {
            'January': 1, 'Jan': 1, 'February': 2, 'Feb': 2, 'March': 3, 'Mar': 3,
            'April': 4, 'Apr': 4, 'May': 5, 'June': 6, 'Jun': 6,
            'July': 7, 'Jul': 7, 'August': 8, 'Aug': 8, 'September': 9, 'Sep': 9,
            'October': 10, 'Oct': 10, 'November': 11, 'Nov': 11, 'December': 12, 'Dec': 12
        }

        # Extract month, start day, and year
        # Patterns: "October 23-24, 2025" or "Oct 28-30, 2025"
        pattern = r'(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d+)(?:-\d+)?,?\s*(\d{4})'
        match = re.search(pattern, visit_period, re.IGNORECASE)

        if match:
            month_name = match.group(1)
            start_day = int(match.group(2))
            year = int(match.group(3))
            month_num = month_map.get(month_name.capitalize()) or month_map.get(month_name[:3].capitalize())

            if month_num:
                return datetime(year, month_num, start_day)

        return None

    def format_date_range(self, date_string: str) -> str:
        """Convert date format to shorter month format (e.g., 'October 23-24, 2025' -> 'Oct 23-24')"""
        import re

        # Handle formats like "October 23-24, 2025"
        month_map = {
            'January': 'Jan', 'February': 'Feb', 'March': 'Mar', 'April': 'Apr',
            'May': 'May', 'June': 'Jun', 'July': 'Jul', 'August': 'Aug',
            'September': 'Sep', 'October': 'Oct', 'November': 'Nov', 'December': 'Dec'
        }

        # Replace full month names with abbreviated ones and remove year
        for full_month, short_month in month_map.items():
            if full_month in date_string:
                # Remove year and replace month
                formatted = re.sub(r',?\s*20\d{2}', '', date_string)  # Remove year
                formatted = formatted.replace(full_month, short_month)
                return formatted

        return date_string  # Return as-is if no transformation needed

    def parse_research_file(self, file_path: Path) -> Dict[str, Any]:
        """Parse a markdown research file and extract structured data."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract basic info from markdown structure
        data = {
            'title': self.extract_title(content),
            'content': content,
            'file_path': file_path
        }

        # Extract sections
        data.update(self.extract_sections(content))

        # Extract metadata fields (like **Category:** etc.)
        data.update(self.extract_metadata(content))

        # Parse visit date for sorting
        if 'visit_period' in data:
            data['visit_date'] = self.parse_visit_date(data['visit_period'])

        return data

    def extract_title(self, content: str) -> str:
        """Extract title from markdown file."""
        match = re.search(r'^# (.+)$', content, re.MULTILINE)
        if match:
            return match.group(1).replace(' Research', '')
        return "Unknown"

    def extract_sections(self, content: str) -> Dict[str, str]:
        """Extract major sections from markdown content."""
        sections = {}

        # Extract metadata from top of file (Visit Period, Duration, etc.)
        visit_period_match = re.search(r'\*\*Visit Period:\*\*\s*(.+)', content)
        if visit_period_match:
            sections['visit_period'] = visit_period_match.group(1).strip()

        duration_match = re.search(r'\*\*Duration:\*\*\s*(.+)', content)
        if duration_match:
            sections['duration'] = duration_match.group(1).strip()

        # Split content into sections
        section_pattern = r'^## (.+)$'
        parts = re.split(section_pattern, content, flags=re.MULTILINE)

        current_section = None
        for i, part in enumerate(parts):
            if i % 2 == 1:  # Section headers
                current_section = part.strip().lower().replace(' ', '_')
            elif current_section and i % 2 == 0:  # Section content
                sections[current_section] = part.strip()

        return sections

    def extract_metadata(self, content: str) -> Dict[str, str]:
        """Extract metadata fields like **Category:** from content."""
        metadata = {}

        # Pattern to match **Field:** value
        metadata_pattern = r'\*\*([^:]+):\*\*\s*(.+?)(?=\n|\*\*|$)'
        matches = re.findall(metadata_pattern, content)

        for field, value in matches:
            field_key = field.lower().replace(' ', '_').replace('&', 'and')
            metadata[field_key] = value.strip()

        return metadata

    def categorize_attraction(self, category_text: str) -> str:
        """Categorize an attraction based on its category text."""
        if not category_text:
            return "Other"

        category_lower = category_text.lower()

        for group_name, keywords in CATEGORY_GROUPS.items():
            if any(keyword in category_lower for keyword in keywords):
                return group_name

        return "Other"

    def discover_routes(self) -> Dict[str, List[Path]]:
        """Discover all route files grouped by destination pairs (origin-to-destination)."""
        routes_by_pair = {}

        if not self.routes_dir.exists():
            return routes_by_pair

        # Find all route folders
        for route_folder in self.routes_dir.glob("*/"):
            if not route_folder.is_dir():
                continue

            # Find route markdown file in the folder
            route_files = list(route_folder.glob("*.md"))
            if not route_files:
                continue

            route_file = route_files[0]  # Assume one main route file per folder
            folder_name = route_folder.name

            # Parse destination pair from folder name: {origin}-to-{destination}-{route-type}-route
            # Example: tokyo-to-fujikawaguchiko-scenic-route
            pattern = r'^(.+?)-to-(.+?)-(?:.+-)?route$'
            match = re.match(pattern, folder_name)

            if match:
                origin = match.group(1)
                destination = match.group(2)
                pair_key = f"{origin}-to-{destination}"

                if pair_key not in routes_by_pair:
                    routes_by_pair[pair_key] = []

                routes_by_pair[pair_key].append(route_file)

        return routes_by_pair

    def parse_route_sections(self, route_file: Path) -> Dict[str, Any]:
        """Parse a route file and extract sections with their attractions."""
        with open(route_file, 'r', encoding='utf-8') as f:
            content = f.read()

        route_data = {
            'title': self.extract_title(content),
            'file_path': route_file,
            'route_folder': route_file.parent.name,
            'content': content,
            'metadata': {}
        }

        # Extract metadata from top of file
        metadata_patterns = {
            'travel_date': r'\*\*Travel Date:\*\*\s*(.+)',
            'transportation': r'\*\*Transportation:\*\*\s*(.+)',
            'route_type': r'\*\*Route Type:\*\*\s*(.+)',
            'route_distance': r'\*\*Route Distance:\*\*\s*(.+)',
            'base_drive_time': r'\*\*Base Drive Time:\*\*\s*(.+)',
        }

        for key, pattern in metadata_patterns.items():
            match = re.search(pattern, content)
            if match:
                route_data['metadata'][key] = match.group(1).strip()

        # Extract sections by detour level
        route_data['sections'] = self.extract_route_sections(content, route_file.parent.name)

        return route_data

    def extract_route_sections(self, content: str, route_folder_name: str) -> Dict[str, List[Dict]]:
        """Extract attraction sections organized by detour level from route content."""
        sections = {
            'on_route': [],
            'short_detour': [],
            'major_detour': []
        }

        # Define section headers to look for
        section_patterns = [
            (r'## On-Route Stops.*?\n', 'on_route'),
            (r'## Short Detour Stops.*?\n', 'short_detour'),
            (r'## Major Detour Stops.*?\n', 'major_detour')
        ]

        # Find each section and extract subsections (### headings)
        for pattern, section_key in section_patterns:
            section_match = re.search(pattern, content, re.IGNORECASE)
            if not section_match:
                continue

            # Find the start of this section
            section_start = section_match.end()

            # Find the end of this section (next ## heading or end of file)
            next_section = re.search(r'\n## ', content[section_start:])
            section_end = section_start + next_section.start() if next_section else len(content)
            section_content = content[section_start:section_end]

            # Extract ### subsections (individual attractions)
            subsection_pattern = r'### (.+?)\n'
            for subsection_match in re.finditer(subsection_pattern, section_content):
                attraction_title = subsection_match.group(1).strip()
                attraction_slug = create_url_slug(attraction_title)

                # Check if attraction file exists
                attraction_file = self.research_dir / "attractions" / route_folder_name / f"{attraction_slug}.md"
                if attraction_file.exists():
                    sections[section_key].append({
                        'title': attraction_title,
                        'slug': attraction_slug,
                        'file_path': attraction_file
                    })

        return sections

    def get_attraction_data(self, destination_slug: str) -> List[Dict]:
        """Get attraction data with category information for a destination."""
        attractions_data = []
        attraction_dir = self.research_dir / "attractions" / destination_slug

        if not attraction_dir.exists():
            return attractions_data

        for attraction_file in attraction_dir.glob("*.md"):
            attraction_data = self.parse_research_file(attraction_file)

            if attraction_data:
                # Use filename as source of truth for slug
                slug = attraction_file.stem
                attraction_title = attraction_data.get('title', slug.replace('-', ' ').title())
                category_text = attraction_data.get('category', '')
                category_group = self.categorize_attraction(category_text)

                attractions_data.append({
                    'title': attraction_title,
                    'slug': slug,
                    'category': category_group,
                    'original_category': category_text,
                    'file_path': str(attraction_file)
                })

        return attractions_data

    def organize_attractions_by_category(self, attractions_data: List[Dict]) -> Dict[str, List[Dict]]:
        """Organize attractions by category in display order."""
        categorized = {}

        # Group attractions by category
        for attraction in attractions_data:
            category = attraction['category']
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(attraction)

        # Sort attractions within each category alphabetically
        for category in categorized:
            categorized[category].sort(key=lambda x: x['title'])

        # Return in specified category order
        ordered_categories = {}
        for category in CATEGORY_ORDER:
            if category in categorized:
                ordered_categories[category] = categorized[category]

        # Add any remaining categories not in the predefined order
        for category, attractions in categorized.items():
            if category not in ordered_categories:
                ordered_categories[category] = attractions

        return ordered_categories

    def generate_timeline_entry(self, data: Dict, entry_type: str, order: int,
                              date: datetime, timeline_entries: List[Dict],
                              routes_data: Optional[List[Dict]] = None) -> str:
        """Generate a timeline entry from research data."""

        if entry_type == "destination":
            # Extract visit period and duration from research data
            visit_period = data.get('visit_period', '').replace('**', '').replace('Visit Period:', '').strip()
            duration_raw = data.get('duration', '').replace('**', '').replace('Duration:', '').strip()

            # Use actual dates and duration from research, with fallbacks
            title = data['title']  # Always use just the destination name
            date_range_display = self.format_date_range(visit_period) if visit_period else ""

            duration = duration_raw if duration_raw else '4 days'

            # Build extra fields with place
            destination_slug = create_url_slug(data["title"])
            extra_fields = f'place = "{destination_slug}"'

            # Generate content from research sections
            content = self.generate_destination_content(data)

            # Source files
            source_files = str(data['file_path'].relative_to(self.research_dir))

        elif entry_type == "journey":
            from_city = data.get('from', 'Unknown')
            to_city = data.get('to', 'Unknown')
            title = f"{from_city.title()} to {to_city.title()}"
            date_range_display = data.get('travel_date', '')
            duration = "Travel day"
            extra_fields = f'from = "{from_city.lower()}"\nto = "{to_city.lower()}"'

            # Generate content from route research (multiple routes possible)
            content = self.generate_journey_content(routes_data or [])

            # Source files - list all route files
            if routes_data:
                source_list = [str(r['file_path'].relative_to(self.research_dir)) for r in routes_data]
                source_files = ', '.join(source_list)
            else:
                source_files = "No route files"

        # Get navigation data for template
        nav_data = self.get_navigation_data(order, timeline_entries)

        # Add navigation data to extra fields
        for key, value in nav_data.items():
            extra_fields += f'\n{key} = "{value}"'

        return TIMELINE_ENTRY_TEMPLATE.format(
            title=title,
            description=data.get('description', f"{entry_type.title()} in our Japan journey"),
            date=date.strftime("%Y-%m-%d"),
            weight=order,
            order=order,
            entry_type=entry_type,
            date_range=date_range_display,
            duration=duration,
            extra_fields=extra_fields,
            content=content,
            source_files=source_files
        )

    def generate_destination_content(self, data: Dict) -> str:
        """Generate destination timeline content from research."""
        # Get the original content and extract everything after the metadata section
        original_content = data.get('content', '')

        # Find the start of the actual content (after title and metadata)
        content_start_match = re.search(r'\n## Basic Information', original_content)
        if content_start_match:
            # Extract content from Basic Information onward
            main_content = original_content[content_start_match.start():]
        else:
            # Fallback to basic information section
            main_content = f"## Overview\n\n{data.get('basic_information', 'Information about this destination.')}"

        # Find attractions for this destination and add them
        destination_slug = create_url_slug(data["title"])
        attractions_data = self.get_attraction_data(destination_slug)

        # Build categorized attractions section
        attractions_section = ""
        if attractions_data:
            categorized_attractions = self.organize_attractions_by_category(attractions_data)

            for category, attractions in categorized_attractions.items():
                if attractions:  # Only add categories that have attractions
                    attractions_section += f"\n## {category}\n\n"
                    for attraction in attractions:
                        title = attraction['title']
                        slug = attraction['slug']
                        original_category = attraction['original_category']
                        attractions_section += f"- **[{title}](/attractions/{slug}/)** - {original_category}\n"

        # Insert attractions section after overview if it exists
        if "## Basic Information" in main_content:
            main_content = main_content.replace("## Basic Information", "## Overview") + attractions_section
        else:
            main_content = main_content + attractions_section

        return main_content.strip()

    def generate_journey_content(self, routes_data: List[Dict]) -> str:
        """Generate journey timeline content with links to route option pages and attraction lists."""
        if not routes_data:
            return "## The Journey\n\nRoute information not yet available."

        content = "## Route Options\n\n"

        # If only one route
        if len(routes_data) == 1:
            route = routes_data[0]
            route_folder = route.get('route_folder', '')
            route_title = route['title'].replace(' Research', '')
            metadata = route.get('metadata', {})

            content += f"**[{route_title}](/routes/{route_folder}/)**\n\n"

            if metadata:
                details = []
                if 'route_distance' in metadata:
                    details.append(f"Distance: {metadata['route_distance']}")
                if 'base_drive_time' in metadata:
                    details.append(f"Drive Time: {metadata['base_drive_time']}")
                if details:
                    content += f"*{' | '.join(details)}*\n\n"

                if 'route_type' in metadata:
                    content += f"Type: {metadata['route_type']}\n\n"

            # Extract first paragraph from route overview
            route_content = route.get('content', '')
            overview_match = re.search(r'## Route Overview\s*\n(.*?)(?=\n## |\Z)', route_content, re.DOTALL)
            if overview_match:
                overview_text = overview_match.group(1).strip()
                first_para = overview_text.split('\n\n')[0] if overview_text else ''
                if first_para:
                    content += f"{first_para}\n\n"

            # Add attraction lists organized by detour level
            content += self.generate_single_route_content(route)

        else:
            # Multiple routes - present as options
            content += f"This journey offers {len(routes_data)} route alternatives:\n\n"

            for i, route in enumerate(routes_data, 1):
                route_folder = route.get('route_folder', '')
                route_title = route['title'].replace(' Research', '')
                metadata = route.get('metadata', {})

                content += f"### **[{route_title}](/routes/{route_folder}/)**\n\n"

                if metadata:
                    details = []
                    if 'route_distance' in metadata:
                        details.append(f"Distance: {metadata['route_distance']}")
                    if 'base_drive_time' in metadata:
                        details.append(f"Drive Time: {metadata['base_drive_time']}")
                    if details:
                        content += f"*{' | '.join(details)}*\n\n"

                    if 'route_type' in metadata:
                        content += f"Type: {metadata['route_type']}\n\n"

                # Extract first paragraph from route overview
                route_content = route.get('content', '')
                overview_match = re.search(r'## Route Overview\s*\n(.*?)(?=\n## |\Z)', route_content, re.DOTALL)
                if overview_match:
                    overview_text = overview_match.group(1).strip()
                    first_para = overview_text.split('\n\n')[0] if overview_text else ''
                    if first_para:
                        content += f"{first_para}\n\n"

                # Add attraction lists organized by detour level
                content += self.generate_single_route_content(route)

                if i < len(routes_data):
                    content += "\n---\n\n"

        return content.strip()

    def generate_single_route_content(self, route_data: Dict) -> str:
        """Generate content for a single route with its attractions organized by detour level."""
        content = ""
        sections = route_data.get('sections', {})
        route_folder = route_data.get('route_folder', '')

        # Display attractions by detour level
        detour_sections = [
            ('on_route', 'On-Route Stops', 'Stops directly on the route with no detour'),
            ('short_detour', 'Short Detour Stops', '15-30 minutes off the main route'),
            ('major_detour', 'Major Detour Stops', '30+ minutes detour, significant attractions')
        ]

        for section_key, section_title, section_desc in detour_sections:
            attractions = sections.get(section_key, [])
            if attractions:
                content += f"**{section_title}** *({section_desc})*\n\n"
                for attraction in attractions:
                    # Route attractions use /routes/{route-folder}/{slug}/ URLs
                    content += f"- **[{attraction['title']}](/routes/{route_folder}/{attraction['slug']}/)**\n"
                content += "\n"

        return content

    def get_navigation_data(self, order: int, timeline_entries: List[Dict]) -> Dict:
        """Get navigation data for timeline entries to pass to template."""
        nav_data = {}

        # Find previous and next entries
        for entry in timeline_entries:
            if entry['order'] == order - 1:
                nav_data['previous_entry'] = entry['filename']
                nav_data['previous_title'] = entry['title']
            elif entry['order'] == order + 1:
                nav_data['next_entry'] = entry['filename']
                nav_data['next_title'] = entry['title']

        return nav_data

    def generate_all_content(self):
        """Generate all timeline content from research files, interleaving destinations and journeys."""

        # Remove existing timeline content
        for file in self.output_dir.glob("??-*.md"):
            file.unlink()

        print("🧹 Cleared existing timeline content")

        # 1. Collect all destination files and their data
        destination_data_list = []
        for research_file in (self.research_dir / "destinations").glob("*.md"):
            # Skip non-destination files
            if research_file.name in ['destinations-todo.md', '_index.md']:
                continue

            destination_data = self.parse_research_file(research_file)
            destination_data_list.append((research_file, destination_data))

        # Sort destinations by visit date
        destination_data_list.sort(key=lambda x: x[1].get('visit_date') or datetime.min)

        # 2. Discover and parse all routes
        routes_by_pair = self.discover_routes()
        print(f"📍 Found {sum(len(routes) for routes in routes_by_pair.values())} route files across {len(routes_by_pair)} journeys")

        parsed_routes = {}
        for pair_key, route_files in routes_by_pair.items():
            parsed_routes[pair_key] = [self.parse_route_sections(rf) for rf in route_files]

        # 3. Build complete timeline structure (destinations + journeys)
        timeline_entries = []
        order = 1
        start_date = datetime(2025, 4, 1)

        for i, (research_file, destination_data) in enumerate(destination_data_list):
            destination_slug = research_file.stem

            # Check if this is the first destination and if there's a route leading to it
            if i == 0:
                # Look for any route that ends with this destination
                incoming_routes = [
                    (pair_key, routes)
                    for pair_key, routes in parsed_routes.items()
                    if pair_key.endswith(f"-to-{destination_slug}")
                ]

                if incoming_routes:
                    # Extract origin from the first incoming route
                    pair_key, routes = incoming_routes[0]
                    origin_slug = pair_key.replace(f"-to-{destination_slug}", "")

                    # Add journey entry before first destination
                    journey_filename = f"{order:02d}-{pair_key}"
                    timeline_entries.append({
                        'order': order,
                        'type': 'journey',
                        'filename': journey_filename,
                        'title': f"{origin_slug.title()} to {destination_data['title']}",
                        'from': origin_slug,
                        'to': destination_slug,
                        'routes_data': routes,
                        'date': start_date - timedelta(days=1)  # Day before first destination
                    })
                    order += 1

            # Add destination entry
            timeline_entries.append({
                'order': order,
                'type': 'destination',
                'filename': f"{order:02d}-{destination_slug}",
                'title': destination_data['title'],
                'slug': destination_slug,
                'data': destination_data,
                'file': research_file,
                'date': destination_data.get('visit_date') or (start_date + timedelta(days=i*4))
            })
            order += 1

            # Check if there's a journey to the next destination
            if i < len(destination_data_list) - 1:
                next_destination_slug = destination_data_list[i+1][0].stem
                pair_key = f"{destination_slug}-to-{next_destination_slug}"

                if pair_key in parsed_routes:
                    # Add journey entry
                    journey_filename = f"{order:02d}-{pair_key}"
                    timeline_entries.append({
                        'order': order,
                        'type': 'journey',
                        'filename': journey_filename,
                        'title': f"{destination_data['title']} to {destination_data_list[i+1][1]['title']}",
                        'from': destination_slug,
                        'to': next_destination_slug,
                        'routes_data': parsed_routes[pair_key],
                        'date': destination_data.get('visit_date') or (start_date + timedelta(days=i*4))
                    })
                    order += 1

        # 4. Generate timeline entry files
        for entry in timeline_entries:
            if entry['type'] == 'destination':
                content = self.generate_timeline_entry(
                    entry['data'],
                    "destination",
                    entry['order'],
                    entry['date'],
                    timeline_entries
                )
            else:  # journey
                # Create journey data dict
                journey_data = {
                    'from': entry['from'],
                    'to': entry['to'],
                    'travel_date': '',
                    'description': f"Journey from {entry['title']}"
                }
                content = self.generate_timeline_entry(
                    journey_data,
                    "journey",
                    entry['order'],
                    entry['date'],
                    timeline_entries,
                    routes_data=entry['routes_data']
                )

            output_file = self.output_dir / f"{entry['filename']}.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Generated {entry['type']} entry: {output_file}")

        # 5. Generate attraction pages with timeline order mapping
        destination_order_map = {
            entry['slug']: entry['order']
            for entry in timeline_entries
            if entry['type'] == 'destination'
        }
        self.generate_attraction_pages(destination_order_map, timeline_entries)

        # 6. Generate index file
        self.generate_index_file()

        print(f"\n🎉 Generated {len(timeline_entries)} timeline entries ({sum(1 for e in timeline_entries if e['type']=='destination')} destinations + {sum(1 for e in timeline_entries if e['type']=='journey')} journeys)!")

    def generate_attraction_pages(self, destination_order_map: Dict[str, int], timeline_entries: List[Dict]):
        """Generate attraction pages from research files (both destinations and routes)."""
        attractions_dir = self.output_dir / "attractions"
        attractions_dir.mkdir(exist_ok=True)

        # Create routes directory for route attractions
        routes_dir = self.output_dir / "routes"
        routes_dir.mkdir(exist_ok=True)

        # Process attractions from all folders (destinations and routes)
        attractions_research_dir = self.research_dir / "attractions"

        # Build a map of journey entries for route attraction linking
        journey_order_map = {
            f"{entry['from']}-to-{entry['to']}" if entry['type'] == 'journey' else None: entry['order']
            for entry in timeline_entries
            if entry['type'] == 'journey'
        }

        # First pass: collect all attractions by folder and get category order
        attractions_by_folder = {}
        route_folders = set()  # Track route folders for index generation

        for folder in attractions_research_dir.glob("*/"):
            if folder.is_dir():
                folder_name = folder.name

                # Determine if this is a destination or route folder
                is_route = '-to-' in folder_name and '-route' in folder_name

                # Track route folders for index generation
                if is_route:
                    route_folders.add(folder_name)

                # Get attraction data with category information
                attractions_data = self.get_attraction_data(folder_name)

                # Organize attractions by category in display order
                categorized_attractions = self.organize_attractions_by_category(attractions_data)

                # Create flat ordered list following the category order
                attractions_list = []
                for category in CATEGORY_ORDER:
                    if category in categorized_attractions:
                        for attraction_data in categorized_attractions[category]:
                            # Load the full research file data for each attraction
                            attraction_file = self.research_dir / "attractions" / folder_name / f"{attraction_data['slug']}.md"
                            if attraction_file.exists():
                                full_data = self.parse_research_file(attraction_file)
                                attractions_list.append({
                                    'title': attraction_data['title'],
                                    'slug': attraction_data['slug'],
                                    'file': attraction_file,
                                    'data': full_data,
                                    'is_route': is_route
                                })

                # Add any remaining categories not in the predefined order
                for category, attractions in categorized_attractions.items():
                    if category not in CATEGORY_ORDER:
                        for attraction_data in attractions:
                            attraction_file = self.research_dir / "attractions" / folder_name / f"{attraction_data['slug']}.md"
                            if attraction_file.exists():
                                full_data = self.parse_research_file(attraction_file)
                                attractions_list.append({
                                    'title': attraction_data['title'],
                                    'slug': attraction_data['slug'],
                                    'file': attraction_file,
                                    'data': full_data,
                                    'is_route': is_route
                                })

                attractions_by_folder[folder_name] = attractions_list

        # Build a map of route data by folder name for route page generation
        route_data_by_folder = {}
        journey_refs_by_folder = {}

        for entry in timeline_entries:
            if entry['type'] == 'journey' and 'routes_data' in entry:
                journey_ref = entry['filename']
                journey_title = entry['title']
                for route_data in entry['routes_data']:
                    folder_name = route_data.get('route_folder', '')
                    if folder_name:
                        route_data_by_folder[folder_name] = route_data
                        journey_refs_by_folder[folder_name] = (journey_ref, journey_title)

        # Generate _index.md files for all route sections with full route content
        for route_name in route_folders:
            route_output_dir = routes_dir / route_name
            route_output_dir.mkdir(exist_ok=True)

            # Get route data and journey reference for this route
            route_data = route_data_by_folder.get(route_name)
            journey_info = journey_refs_by_folder.get(route_name, ("", ""))
            journey_ref, journey_title = journey_info

            self.generate_route_section_index(
                route_output_dir,
                route_name,
                route_data=route_data,
                journey_entry_ref=journey_ref,
                journey_title=journey_title
            )
            print(f"✅ Generated route section index: {route_output_dir / '_index.md'}")

        # Second pass: generate attraction files with navigation
        for folder_name, attractions_list in attractions_by_folder.items():
            for i, attraction in enumerate(attractions_list):
                data = attraction['data']
                slug = attraction['slug']
                research_file = attraction['file']

                # Calculate navigation
                previous_attraction = ""
                next_attraction = ""
                previous_title = ""
                next_title = ""

                if i > 0:
                    previous_attraction = attractions_list[i-1]['slug']
                    previous_title = attractions_list[i-1]['title']

                if i < len(attractions_list) - 1:
                    next_attraction = attractions_list[i+1]['slug']
                    next_title = attractions_list[i+1]['title']

                # Get the original content and extract everything after the metadata section
                original_content = data.get('content', '')

                # Find the start of the actual content (after title and metadata)
                content_start_match = re.search(r'\n## Basic Information', original_content)
                if content_start_match:
                    # Extract content from Basic Information onward
                    attraction_content = original_content[content_start_match.start():]
                    # Replace first section header for consistency
                    attraction_content = attraction_content.replace("## Basic Information", "## About", 1)
                else:
                    attraction_content = "## About\n\nAttraction information not available."

                # Determine timeline entry reference and output path
                is_route = attraction.get('is_route', False)
                if is_route:
                    # Extract route pair from folder name for journey linking
                    route_pair = folder_name.replace('-route', '').replace('-scenic', '').replace('-main', '').replace('-coastal', '')
                    # Find the journey order number
                    timeline_order = journey_order_map.get(route_pair, 1)
                    timeline_ref = f'{timeline_order:02d}-{route_pair}'
                    place_ref = route_pair

                    # Route attractions go to /routes/{route-name}/ directory
                    route_output_dir = routes_dir / folder_name
                    route_output_dir.mkdir(exist_ok=True)
                    attraction_file = route_output_dir / f"{slug}.md"
                else:
                    # Destination attraction
                    timeline_order = destination_order_map.get(folder_name, 1)
                    timeline_ref = f'{timeline_order:02d}-{folder_name}'
                    place_ref = folder_name

                    # Destination attractions go to /attractions/ directory
                    attraction_file = attractions_dir / f"{slug}.md"

                content = ATTRACTION_TEMPLATE.format(
                    title=escape_toml_string(data['title']),
                    description=escape_toml_string(f"Detailed guide to {data['title']}"),
                    weight=10,
                    categories='["temples"]',
                    tags='["historic", "cultural"]',
                    location=folder_name.title().replace('-To-', ' to ').replace('-', ' ') + ", Japan",
                    category="Attraction",
                    cost="Varies",
                    best_time="See details",
                    place=place_ref,
                    timeline_entries=f'["{timeline_ref}"]',
                    difficulty="Easy",
                    visit_duration="Varies",
                    previous_attraction=previous_attraction,
                    next_attraction=next_attraction,
                    previous_title=escape_toml_string(previous_title),
                    next_title=escape_toml_string(next_title),
                    content=attraction_content.strip(),
                    source_file=str(research_file.relative_to(self.research_dir))
                )

                with open(attraction_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ Generated {'route' if is_route else 'destination'} attraction: {attraction_file}")

    def generate_index_file(self):
        """Generate the main index file for the timeline."""
        index_content = """+++
title = "Japan Trip 2025 Timeline"
description = "Our chronological journey through Japan - from Tokyo to cultural treasures"
template = "timeline.html"
sort_by = "weight"
+++"""

        index_file = self.output_dir / "_index.md"
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_content)
        print(f"✅ Generated index file: {index_file}")

    def generate_route_page(self, route_data: Dict, journey_entry_ref: str, journey_title: str) -> str:
        """Generate a comprehensive route page from route research file."""
        # Read the full route research file
        route_content = route_data.get('content', '')
        route_title = route_data.get('title', 'Route')
        metadata = route_data.get('metadata', {})

        # Extract route overview paragraph (first paragraph after Route Overview heading)
        overview_match = re.search(r'## Route Overview\s*\n(.*?)(?=\n## |\Z)', route_content, re.DOTALL)
        overview_paragraph = ''
        if overview_match:
            overview_text = overview_match.group(1).strip()
            # Take first paragraph only
            overview_paragraph = overview_text.split('\n\n')[0] if overview_text else ''

        # Extract main content starting from Route Overview section
        content_start_match = re.search(r'\n## Route Overview', route_content)
        if content_start_match:
            main_content = route_content[content_start_match.start():]
        else:
            main_content = "## Route Information\n\nDetailed route information will be available soon."

        # Build frontmatter
        route_type = metadata.get('route_type', 'Scenic')
        transportation = metadata.get('transportation', 'Car')
        distance = metadata.get('route_distance', 'N/A')
        drive_time = metadata.get('base_drive_time', 'N/A')

        route_page_content = f"""+++
title = "{escape_toml_string(route_title)}"
description = "Complete guide for {escape_toml_string(route_title)}"
template = "route.html"
weight = 10

[extra]
journey_entry = "{journey_entry_ref}"
journey_title = "{escape_toml_string(journey_title)}"
route_type = "{escape_toml_string(route_type)}"
transportation = "{escape_toml_string(transportation)}"
distance = "{escape_toml_string(distance)}"
drive_time = "{escape_toml_string(drive_time)}"
+++

{main_content.strip()}

---

*Source: {str(route_data['file_path'].relative_to(self.research_dir))}*
"""
        return route_page_content

    def generate_route_section_index(self, route_dir: Path, route_name: str, route_data: Dict = None, journey_entry_ref: str = "", journey_title: str = ""):
        """Generate an _index.md file for a route section with full route research content."""
        if route_data and journey_entry_ref:
            # Generate comprehensive route page
            index_content = self.generate_route_page(route_data, journey_entry_ref, journey_title)
        else:
            # Fallback to simple placeholder (shouldn't happen in normal flow)
            title = route_name.replace('-', ' ').title()
            title = title.replace(' Route', ' Route').replace(' To ', ' to ')
            index_content = f"""+++
title = "{title}"
description = "Attractions and stops along the {title}"
template = "route.html"
sort_by = "weight"
+++

# {title}

This section contains detailed information about attractions and stops along this route."""

        index_file = route_dir / "_index.md"
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_content)

def main():
    parser = argparse.ArgumentParser(description='Generate timeline-based Zola content from research files')
    parser.add_argument('--research', default='research',
                       help='Research directory path (default: research)')
    parser.add_argument('--output', default='site/content',
                       help='Output directory for generated content (default: site/content)')
    parser.add_argument('--clean', action='store_true',
                       help='Clean existing content before generating')

    args = parser.parse_args()

    research_dir = Path(args.research)
    output_dir = Path(args.output)

    if not research_dir.exists():
        print(f"❌ Research directory not found: {research_dir}")
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"🚀 Generating timeline content from {research_dir} to {output_dir}")

    generator = TimelineGenerator(research_dir, output_dir)
    generator.generate_all_content()

    print("\n✨ Content generation complete! Run 'zola serve' to preview the site.")

if __name__ == "__main__":
    main()