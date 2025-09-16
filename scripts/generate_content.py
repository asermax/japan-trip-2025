#!/usr/bin/env python3
"""
Helper script to generate Zola content from research files.
This script will help convert raw research into structured Markdown files.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import argparse

# Template for destination pages
DESTINATION_TEMPLATE = """+++
title = "{title}"
description = "{description}"
weight = {weight}
regions = {regions}
tags = {tags}

[extra]
duration = "{duration}"
best_season = "{best_season}"
+++

# {title}

## Overview
{overview}

## Logistics
- **Getting There**: {getting_there}
- **Accommodation**: {accommodation}
- **Local Transportation**: {local_transport}

## Highlights
{highlights}

## Food & Dining
{food_dining}

## Day Trips
{day_trips}
"""

# Template for journey pages
JOURNEY_TEMPLATE = """+++
title = "{title}"
description = "{description}"
weight = {weight}
tags = {tags}

[extra]
from = "{from_city}"
to = "{to_city}"
distance = "{distance}"
duration = "{duration}"
+++

# {title}

## Route Options
{route_options}

## Transportation
{transportation}

## Scenic Stops
{scenic_stops}

## Timing & Tips
{timing_tips}
"""

# Template for attraction pages
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
+++

# {title}

## About
{about}

## Visiting Information
- **Hours**: {hours}
- **Cost**: {cost}
- **Access**: {access}

## What to Expect
{what_to_expect}

## Tips
{tips}
"""

def create_destination(data, output_dir):
    """Create a destination markdown file from data dict."""
    filename = f"{data['title'].lower().replace(' ', '-')}.md"
    filepath = output_dir / "destinations" / filename

    content = DESTINATION_TEMPLATE.format(**data)

    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Created destination: {filepath}")

def create_journey(data, output_dir):
    """Create a journey markdown file from data dict."""
    filename = f"{data['from_city'].lower().replace(' ', '-')}-to-{data['to_city'].lower().replace(' ', '-')}.md"
    filepath = output_dir / "journey" / filename

    content = JOURNEY_TEMPLATE.format(**data)

    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Created journey: {filepath}")

def create_attraction(data, output_dir):
    """Create an attraction markdown file from data dict."""
    filename = f"{data['title'].lower().replace(' ', '-').replace('/', '-')}.md"
    filepath = output_dir / "discover" / filename

    content = ATTRACTION_TEMPLATE.format(**data)

    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Created attraction: {filepath}")

def main():
    parser = argparse.ArgumentParser(description='Generate Zola content from research data')
    parser.add_argument('--type', choices=['destination', 'journey', 'attraction'],
                       help='Type of content to generate')
    parser.add_argument('--output', default='site/content',
                       help='Output directory for generated content')

    args = parser.parse_args()

    print("Content generation script ready!")
    print("Use this script to convert your research data into Zola markdown files.")
    print("Example usage:")
    print("  python scripts/generate_content.py --type destination")

    # This script provides the structure for future automation
    # You can extend it to read from research files and generate content

if __name__ == "__main__":
    main()