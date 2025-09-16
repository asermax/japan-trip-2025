#!/usr/bin/env python3
"""
Generate timeline-based Zola content from research files.
This script reads structured research files and generates timeline entries, place guides, and attraction pages.
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime, timedelta
import argparse
import markdown
from typing import Dict, List, Any

# Timeline entry template
TIMELINE_ENTRY_TEMPLATE = """+++
title = "{title}"
description = "{description}"
date = {date}
weight = {weight}

[extra]
timeline_order = {order}
type = "{entry_type}"
date_range = "{date_range}"
duration = "{duration}"
{extra_fields}
+++

**{date_range}** | **Duration: {duration}**

{content}

{navigation}

---

*Generated from research: {source_files}*
"""

# Place guide template
PLACE_TEMPLATE = """+++
title = "{title}"
description = "{description}"
weight = {weight}
regions = {regions}
tags = {tags}

[extra]
duration = "{duration}"
best_season = "{best_season}"
timeline_entries = {timeline_entries}
featured_attractions = {featured_attractions}
+++

# {title}

{content}

---

**Timeline Navigation**:
{timeline_links}

*Source: {source_file}*
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

# {title}

{content}

**Navigation**:
- **Timeline**: {timeline_link}
- **Place Guide**: {place_link}

*Source: {source_file}*
"""

class TimelineGenerator:
    def __init__(self, research_dir: Path, output_dir: Path):
        self.research_dir = Path(research_dir)
        self.output_dir = Path(output_dir)
        self.timeline_config = []

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

    def generate_timeline_entry(self, data: Dict, entry_type: str, order: int,
                              date: datetime) -> str:
        """Generate a timeline entry from research data."""

        if entry_type == "destination":
            title = f"Days {order}-{order+3}: {data['title']}"
            duration = data.get('duration', '4 days')
            extra_fields = f'place = "{data["title"].lower()}"'

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

        # Navigation links
        navigation = self.generate_navigation(order, entry_type)

        return TIMELINE_ENTRY_TEMPLATE.format(
            title=title,
            description=data.get('description', f"{entry_type.title()} in our Japan journey"),
            date=date.strftime("%Y-%m-%d"),
            weight=order,
            order=order,
            entry_type=entry_type,
            date_range=f"April {order}-{order+3}" if entry_type == "destination" else f"April {order}",
            duration=duration,
            extra_fields=extra_fields,
            content=content,
            navigation=navigation,
            source_files=str(data['file_path'].relative_to(self.research_dir))
        )

    def generate_destination_content(self, data: Dict) -> str:
        """Generate destination timeline content from research."""
        content = f"""
## Overview

{data.get('basic_information', 'Information about this destination.')}

## Key Districts & Experiences

{data.get('key_districts_&_neighborhoods', 'Various districts and neighborhoods to explore.')}

## Cultural Immersion Plan

{data.get('food_culture', 'Local food culture and dining experiences.')}

## Practical Planning

{data.get('practical_information', 'Transportation and logistics information.')}

## Day Trip Options

{data.get('day_trips_from_' + data['title'].lower(), 'Nearby attractions for day trips.')}
"""
        return content.strip()

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

    def generate_navigation(self, order: int, entry_type: str) -> str:
        """Generate navigation links for timeline entries."""
        nav_parts = []

        if order > 1:
            prev_order = f"{order-1:02d}"
            nav_parts.append(f"## Previous: [Previous Entry](/{prev_order}-*/)")

        next_order = f"{order+1:02d}"
        nav_parts.append(f"## Next: [Next Entry](/{next_order}-*/)")

        return "\n".join(nav_parts)

    def generate_all_content(self):
        """Generate all timeline content from research files."""

        # Remove existing timeline content
        for file in self.output_dir.glob("??-*.md"):
            file.unlink()

        print("🧹 Cleared existing timeline content")

        # Generate timeline entries
        timeline_order = 1
        start_date = datetime(2025, 4, 1)

        # 1. Tokyo (destination)
        if (self.research_dir / "destinations" / "tokyo.md").exists():
            tokyo_data = self.parse_research_file(self.research_dir / "destinations" / "tokyo.md")
            entry = self.generate_timeline_entry(tokyo_data, "destination", timeline_order, start_date)

            output_file = self.output_dir / f"{timeline_order:02d}-tokyo.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(entry)
            print(f"✅ Generated: {output_file}")
            timeline_order += 1

        # 2. Tokyo to Kyoto (journey)
        if (self.research_dir / "routes" / "tokyo-to-kyoto.md").exists():
            route_data = self.parse_research_file(self.research_dir / "routes" / "tokyo-to-kyoto.md")
            route_data['from'] = 'Tokyo'
            route_data['to'] = 'Kyoto'
            entry = self.generate_timeline_entry(route_data, "journey", timeline_order,
                                               start_date + timedelta(days=timeline_order-1))

            output_file = self.output_dir / f"{timeline_order:02d}-tokyo-to-kyoto.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(entry)
            print(f"✅ Generated: {output_file}")
            timeline_order += 1

        # 3. Generate place guides
        self.generate_place_guides()

        # 4. Generate attraction pages
        self.generate_attraction_pages()

        # 5. Generate index file
        self.generate_index_file()

        print(f"\n🎉 Generated {timeline_order-1} timeline entries plus place guides and attractions!")

    def generate_place_guides(self):
        """Generate place guide pages from destination research."""
        places_dir = self.output_dir / "places"
        places_dir.mkdir(exist_ok=True)

        for research_file in (self.research_dir / "destinations").glob("*.md"):
            data = self.parse_research_file(research_file)

            place_content = f"""
{data.get('basic_information', '')}

## Timeline Context

**Our {data['title']} Experience**: [View in Timeline](/{data['title'].lower()}/)

## Logistics

{data.get('practical_information', '')}

## Districts & Areas

{data.get('key_districts_&_neighborhoods', '')}

## Food & Dining

{data.get('food_culture', '')}

## Day Trips

{data.get('day_trips_from_' + data['title'].lower(), '')}
"""

            place_file = places_dir / f"{data['title'].lower()}.md"
            content = PLACE_TEMPLATE.format(
                title=data['title'],
                description=f"Comprehensive guide to {data['title']}",
                weight=10,
                regions='["Unknown"]',
                tags='["destination"]',
                duration="4-5 days",
                best_season="Spring/Fall",
                timeline_entries='[]',
                featured_attractions='[]',
                content=place_content.strip(),
                timeline_links=f"- **Our {data['title']} stay**: [Timeline Entry](/{data['title'].lower()}/)",
                source_file=str(research_file.relative_to(self.research_dir))
            )

            with open(place_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Generated place guide: {place_file}")

    def generate_attraction_pages(self):
        """Generate attraction pages from research files."""
        attractions_dir = self.output_dir / "attractions"
        attractions_dir.mkdir(exist_ok=True)

        for research_file in (self.research_dir / "attractions").glob("*.md"):
            data = self.parse_research_file(research_file)

            attraction_content = f"""
## About

{data.get('basic_information', '')}

{data.get('cultural_&_religious_significance', '')}

## Visiting Information

{data.get('visiting_information', '')}

## What to Expect

{data.get('the_trail_experience', '')}
{data.get('cultural_&_religious_significance', '')}

## Practical Tips

{data.get('practical_visiting_tips', '')}
"""

            slug = data['title'].lower().replace(' ', '-').replace('ō', 'o')
            attraction_file = attractions_dir / f"{slug}.md"

            content = ATTRACTION_TEMPLATE.format(
                title=data['title'],
                description=f"Detailed guide to {data['title']}",
                weight=10,
                categories='["temples"]',
                tags='["historic", "cultural"]',
                location="Kyoto, Japan",
                category="Temple",
                cost="Free",
                best_time="Early morning",
                place="kyoto",
                timeline_entries='["03-kyoto"]',
                difficulty="Easy",
                visit_duration="2-3 hours",
                content=attraction_content.strip(),
                timeline_link="[Kyoto Timeline](/03-kyoto/)",
                place_link="[Kyoto Guide](/places/kyoto/)",
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