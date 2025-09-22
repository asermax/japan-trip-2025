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

[extra]
location = "{location}"
category = "{category}"
cost = "{cost}"
best_time = "{best_time}"
place = "{place}"
timeline_entries = {timeline_entries}
difficulty = "{difficulty}"
duration = "{visit_duration}"
+++

{content}

**Navigation**:
- **Timeline**: {timeline_link}

*Source: {source_file}*
"""

class TimelineGenerator:
    def __init__(self, research_dir: Path, output_dir: Path):
        self.research_dir = Path(research_dir)
        self.output_dir = Path(output_dir)
        self.timeline_config = []

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

    def find_destination_attractions(self, destination_slug: str) -> List[str]:
        """Find attractions for a destination using the folder structure."""
        attractions = []
        attraction_dir = self.research_dir / "attractions" / destination_slug

        if not attraction_dir.exists():
            return attractions

        for attraction_file in attraction_dir.glob("*.md"):
            # Parse the attraction file to get the title
            attraction_data = self.parse_research_file(attraction_file)
            attraction_title = attraction_data.get('title', attraction_file.stem.replace('-', ' ').title())
            attractions.append(attraction_title)

        return attractions

    def generate_timeline_entry(self, data: Dict, entry_type: str, order: int,
                              date: datetime, timeline_entries: List[Dict]) -> str:
        """Generate a timeline entry from research data."""

        if entry_type == "destination":
            # Extract visit period and duration from research data
            visit_period = data.get('visit_period', '').replace('**', '').replace('Visit Period:', '').strip()
            duration_raw = data.get('duration', '').replace('**', '').replace('Duration:', '').strip()

            # Use actual dates and duration from research, with fallbacks
            title = data['title']  # Always use just the destination name
            date_range_display = self.format_date_range(visit_period) if visit_period else ""

            duration = duration_raw if duration_raw else '4 days'

            # Find related attractions for this destination
            destination_slug = create_url_slug(data["title"])
            attractions = self.find_destination_attractions(destination_slug)

            # Build extra fields with place and highlights
            extra_fields = f'place = "{destination_slug}"'
            if attractions:
                highlights_str = ', '.join(f'"{attraction}"' for attraction in attractions)
                extra_fields += f'\nhighlights = [{highlights_str}]'

            # Generate content from research sections
            content = self.generate_destination_content(data)

        elif entry_type == "journey":
            from_city = data.get('from', 'Unknown')
            to_city = data.get('to', 'Unknown')
            title = f"Day {order}: {from_city} to {to_city}"
            duration = "Travel day"
            extra_fields = f'from = "{from_city.lower()}"\nto = "{to_city.lower()}"'

            # Generate content from route research
            content = self.generate_journey_content(data)

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
            source_files=str(data['file_path'].relative_to(self.research_dir))
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
        attractions = self.find_destination_attractions(destination_slug)

        # Build attractions section
        attractions_section = ""
        if attractions:
            attractions_section = "\n## Featured Attractions\n\n"
            for attraction in attractions:
                attraction_slug = create_url_slug(attraction)
                attractions_section += f"- **[{attraction}](/attractions/{attraction_slug}/)** - {attraction} detailed guide\n"

        # Insert attractions section after overview if it exists
        if "## Basic Information" in main_content:
            main_content = main_content.replace("## Basic Information", "## Overview") + attractions_section
        else:
            main_content = main_content + attractions_section

        return main_content.strip()

    def generate_journey_content(self, data: Dict) -> str:
        """Generate journey timeline content from research."""
        content = f"""
## The Journey

{data.get('route_overview', 'Transportation route information.')}

## Transportation Options

{data.get('shinkansen_options', 'Various transportation methods available.')}

## Scenic Highlights

{data.get('scenic_highlights', 'Beautiful sights along the journey.')}

## Travel Tips

{data.get('travel_tips_&_strategies', 'Practical advice for the journey.')}
"""
        return content.strip()

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
        """Generate all timeline content from research files."""

        # Remove existing timeline content
        for file in self.output_dir.glob("??-*.md"):
            file.unlink()

        print("🧹 Cleared existing timeline content")

        # Generate timeline entries dynamically from all destination files
        timeline_order = 1
        start_date = datetime(2025, 4, 1)

        # Collect all destination files and their data
        destination_data_list = []
        for research_file in (self.research_dir / "destinations").glob("*.md"):
            # Skip non-destination files
            if research_file.name in ['destinations-todo.md', '_index.md']:
                continue

            destination_data = self.parse_research_file(research_file)
            destination_data_list.append((research_file, destination_data))

        # Sort destinations by visit date
        destination_data_list.sort(key=lambda x: x[1].get('visit_date') or datetime.min)

        # Build complete timeline entries list for navigation
        timeline_entries = []
        for i, (research_file, destination_data) in enumerate(destination_data_list, 1):
            destination_slug = research_file.stem
            filename = f"{i:02d}-{destination_slug}"
            timeline_entries.append({
                'order': i,
                'filename': filename,
                'title': destination_data['title'],
                'slug': destination_slug
            })

        # Process destinations in chronological order
        for i, (research_file, destination_data) in enumerate(destination_data_list, 1):
            entry = self.generate_timeline_entry(destination_data, "destination", i,
                                               start_date + timedelta(days=(i-1)*4), timeline_entries)

            # Create timeline filename from destination name
            destination_slug = research_file.stem
            output_file = self.output_dir / f"{i:02d}-{destination_slug}.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(entry)
            print(f"✅ Generated timeline entry: {output_file}")

        # 3. Generate attraction pages
        self.generate_attraction_pages()

        # 5. Generate index file
        self.generate_index_file()

        print(f"\n🎉 Generated {timeline_order-1} timeline entries and attractions!")

    def generate_attraction_pages(self):
        """Generate attraction pages from research files."""
        attractions_dir = self.output_dir / "attractions"
        attractions_dir.mkdir(exist_ok=True)

        # Process attractions from all destination folders
        attractions_research_dir = self.research_dir / "attractions"
        for destination_folder in attractions_research_dir.glob("*/"):
            if destination_folder.is_dir():
                for research_file in destination_folder.glob("*.md"):
                    data = self.parse_research_file(research_file)

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

                    slug = create_url_slug(data['title'])
                    attraction_file = attractions_dir / f"{slug}.md"

                    content = ATTRACTION_TEMPLATE.format(
                        title=data['title'],
                        description=f"Detailed guide to {data['title']}",
                        weight=10,
                        categories='["temples"]',
                        tags='["historic", "cultural"]',
                        location=destination_folder.name.title() + ", Japan",
                        category="Temple",
                        cost="Free",
                        best_time="Early morning",
                        place=destination_folder.name,
                        timeline_entries=f'["01-{destination_folder.name}"]',
                        difficulty="Easy",
                        visit_duration="2-3 hours",
                        content=attraction_content.strip(),
                        timeline_link=f"[{destination_folder.name.title()} Timeline](/01-{destination_folder.name}/)",
                        source_file=str(research_file.relative_to(self.research_dir))
                    )

                    with open(attraction_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"✅ Generated attraction: {attraction_file}")

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