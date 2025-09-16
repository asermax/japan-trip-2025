# Japan Trip 2025 Research Project

This project is designed to research, organize, and present information about our upcoming Japan trip using AI tools and Zola static site generator with a **timeline-based approach**.

## Project Structure

```
japan-trip-2025/
   research/               # Raw research data and notes
      destinations/       # City/town research
      routes/            # Travel legs between destinations
      attractions/       # POI research organized by type
      state/             # Intermediate state files for research workflow
      trusted-resources.md # Verified sources for research
   site/                  # Zola website with Anatole theme
      config.toml        # Site configuration with theme settings
      content/           # Generated Markdown content organized by timeline
         XX-*.md         # Timeline entries (01-tokyo.md, 02-tokyo-to-kyoto.md, etc.)
         places/         # Detailed destination guides
         attractions/    # Individual attraction pages
         _index.md       # Main timeline homepage
      templates/         # Custom timeline templates
         timeline.html   # Timeline section listing
         timeline-entry.html # Individual timeline entries
      themes/            # Anatole-zola theme
         anatole-zola/   # Blog-focused theme adapted for travel
      static/            # CSS, images, JS from theme
      sass/              # SCSS files
   scripts/               # Content generation automation
      generate_timeline.py # Main content generation script
   CLAUDE.md             # This documentation file
```

## Content Organization (Timeline Approach)

### Primary Content Structure:

1. **Timeline** (`/timeline/`)
   - **Purpose**: Chronological journey from arrival to departure
   - **Format**: Day-by-day or leg-by-leg entries (Place ⇒ Journey ⇒ Place sequence)
   - **Navigation**: Sequential with previous/next links
   - **Cross-links**: References to detailed place and attraction guides

2. **Places** (`/places/`)
   - **Purpose**: Comprehensive destination information
   - **Content**: Logistics, culture, attractions, food, day trips
   - **Integration**: Links to timeline entries and specific attractions
   - **Scope**: Cities, towns, and regions we'll visit

3. **Attractions** (`/attractions/`)
   - **Purpose**: Detailed guides to specific experiences
   - **Content**: Cultural context, visiting info, practical tips
   - **Integration**: Links back to places and timeline entries
   - **Categories**: Temples, markets, districts, natural beauty

### Content Generation:

The site uses automated content generation from research files:
- Research files in structured markdown format
- Automatic timeline entry creation with cross-linking
- Generated place guides and attraction pages
- Index page with timeline overview

## Content Templates

### Timeline Entry Template
```markdown
+++
title = "Days X-Y: Destination" or "Day X: Origin to Destination"
description = "Brief description of this timeline segment"
date = 2025-04-01
weight = 1

[extra]
timeline_order = 1
type = "destination" or "journey"
date_range = "April 1-5"
duration = "5 days" or "Travel day"
place = "tokyo" # for destinations
from = "tokyo" # for journeys
to = "kyoto" # for journeys
highlights = ["attraction1", "attraction2"]
previous_entry/previous_leg = "previous-timeline-slug"
next_entry/next_leg = "next-timeline-slug"
+++

# Timeline Entry Title

**Date Range** | **Duration**

Content with links to [place guides](/places/place-name/) and [attractions](/attractions/attraction-name/).

## Navigation
Previous: [Previous Entry](/timeline/previous/)
Next: [Next Entry](/timeline/next/)
```

### Place Guide Template
```markdown
+++
title = "Place Name"
description = "Comprehensive destination guide"
weight = 10
regions = ["Region Name"]
tags = ["descriptive", "tags"]

[extra]
duration = "X days"
best_season = "Season"
timeline_entries = ["timeline-slug1", "timeline-slug2"]
featured_attractions = ["attraction1", "attraction2"]
+++

# Place Name

Comprehensive information with links to:
- Timeline entries: [Our Visit](/timeline/entry-slug/)
- Related attractions: [Attraction Name](/attractions/attraction-slug/)

## Sections:
- Overview & Cultural Context
- Logistics (transport, accommodation)
- Districts & Areas
- Major Attractions
- Food & Dining
- Day Trips
- Practical Tips
- Timeline Integration
```

### Attraction Guide Template
```markdown
+++
title = "Attraction Name"
description = "Detailed attraction guide"
weight = 10
categories = ["temples", "food", "districts", "nature"]
tags = ["specific", "descriptive", "tags"]

[extra]
location = "City, Prefecture"
category = "Temple/Market/District/etc"
cost = "Free/¥XXX"
best_time = "Morning/Season/etc"
place = "parent-place-slug"
timeline_entries = ["timeline-slug"]
difficulty = "Easy/Moderate/Challenging"
duration = "X hours"
+++

# Attraction Name

Detailed guide with:
- Cultural significance and context
- Practical visiting information
- What to expect
- Photography tips
- Cultural etiquette
- Timeline and place connections

## Navigation Links:
- Timeline: [Timeline Entry](/timeline/entry-slug/)
- Place: [Place Guide](/places/place-slug/)
- Related: [Other Attractions](/attractions/related/)
```

## Cross-Linking System

### Timeline → Places → Attractions
Each timeline entry links to:
- Detailed place guides for comprehensive information
- Specific attractions mentioned in the timeline
- Previous/next timeline entries for navigation

### Places ↔ Attractions
Place guides include:
- List of featured attractions with brief descriptions
- Links to detailed attraction pages
- Reference to relevant timeline entries

Attraction pages include:
- Link back to parent place guide
- Reference to timeline entry where featured
- Links to related attractions

### Archive Integration
- Complete directory accessible from any page
- Category-based browsing (temples, food, districts, nature)
- Regional organization (Kanto, Kansai, etc.)
- Search and filter capabilities through taxonomies

## Workflow

### Research Phase
1. Use AI tools (including Gemini with `-p` flag) for specialized research
2. Consult trusted resources (see `research/trusted-resources.md`)
3. Maintain detailed source citations for all information
4. Save raw research in `/research/` folders organized by type

### Content Creation Phase
1. Run `python scripts/generate_timeline.py` to generate content from research files
2. Script automatically creates timeline entries, place guides, and attraction pages
3. All content follows consistent frontmatter templates
4. Cross-linking between timeline, places, and attractions handled automatically
5. Source citations maintained from research files

### Site Management
1. Use Anatole theme for clean, blog-focused design
2. Leverage Zola's taxonomies (tags, categories, regions)
3. Build and test locally with `zola serve`
4. Deploy using `zola build`

## Commands

### Content Generation & Development
```bash
# Generate content from research files
python scripts/generate_timeline.py --research research --output site/content

# Local development
cd site
zola serve          # Local development server (default port 1111)
zola serve --port XXXX  # Custom port
zola check          # Validate content and templates
zola build          # Generate static site
```

### Content Management
```bash
# View structure
tree content/

# Check build output
tree public/

# Git operations
git status
git add .
git commit -m "description"
```

## Taxonomies & Organization

The site uses taxonomies for content organization:

- **tags**: General descriptors (food, temple, scenic, historic, etc.)
- **categories**: Content types (temples, food, districts, nature)
- **regions**: Geographic areas (Kanto, Kansai, etc.)

Content weight determines ordering within sections:
- Timeline: Chronological by weight/date
- Places: By weight (major destinations first)
- Attractions: By weight (featured attractions first)

## Theme Configuration

### Anatole Theme Features
- Clean, blog-focused design adapted for travel content
- Sidebar navigation with custom menu items
- Responsive design for mobile viewing
- Built-in social sharing and tagging
- Support for custom CSS and templates

### Custom Templates
- `timeline.html`: Section listing with visual timeline
- `timeline-entry.html`: Individual timeline pages with navigation
- Custom CSS for timeline visualization and cross-linking

### Navigation Structure
- **Home**: Timeline overview and site introduction
- **About**: Trip information and methodology
- **Timeline**: Chronological journey navigation
- **Archive**: Complete content directory

## AI Research Integration

### Research Tools & Approach
- **Location Scavenger Agent**: Discovers and catalogs locations/attractions with date-specific events and existing recommendations
- **Location Researcher Agent**: Deep research on specific locations identified by scavenger
- **Gemini Research Agent**: Use `gemini -p` for specialized cultural research, historical context, and local insights
- **Context7 MCP Server**: For up-to-date library documentation
- **Trusted Resources**: Verified sources from `research/trusted-resources.md` for authoritative information
- **WebSearch Tool**: For current information and verification
- **Source Tracking**: Maintain detailed citations for all information

### Specialized Research Agents (`.claude/agents/`)

**Location Scavenger Agent:**
- Identifies information sources and related locations for destinations using WebSearch and trusted resources
- Includes specific travel dates for event research
- References existing recommendations from recommendations-base.md
- Searches for seasonal/date-specific events and festivals
- Cross-references base itinerary suggestions with current offerings
- Provides foundation for detailed research by location researcher agents

**Location Discovery Agent (Gemini-based):**
- Performs the same discovery tasks as Location Scavenger Agent using gemini research capabilities
- Identifies information sources and related locations for destinations
- Searches for seasonal/date-specific events and cultural significance
- References existing recommendations and discovers additional cultural context
- Cross-references findings with authentic local perspectives
- Provides complementary foundation for detailed research phase

**Location Researcher Agent:**
- Conducts detailed research on locations identified by scavenger
- Uses multiple research tools in parallel when possible
- Verifies practical information (hours, costs, accessibility, current status)
- Researches cultural context and visitor experiences

**Gemini Research Agent (`gemini -p`) Usage:**
- Cultural and historical deep-dives beyond web search results
- Local customs, etiquette, and cultural significance research
- Traditional practices and their modern adaptations
- Regional specialties and authentic local experiences
- Cross-cultural context and travel tips from local perspectives

**Trusted Resources Strategy:**
- Prioritize official tourism boards and government sources
- Use verified travel guides and established travel publications
- Cross-reference multiple authoritative sources for accuracy
- Maintain list of reliable sources in `research/trusted-resources.md`
- Document source reliability and last verification dates

### Research Protocol
1. Check multiple sources from trusted resources list
2. Cross-reference information for accuracy
3. Use AI tools to analyze and synthesize information
4. Maintain source citations in proper format
5. Update CLAUDE.md when workflows or tools change

### Destination Research Methodology

**Research Purpose:** Comprehensive cataloging of all available options, attractions, and experiences for each destination. This is **not** itinerary planning - the goal is to research and document everything worth knowing for later reference and decision-making.

The research process consists of two main phases:

**Discovery Phase** (`/discovery [destination]`)
- Deploy parallel agents to identify all information sources and potential attractions
- Generate comprehensive state file with all discovered options organized by interest/significance
- Cross-reference base recommendations with new discoveries
- Create research assignments for detailed investigation of all options

**Detailed Research Phase** (`/research [destination]`)
- Use discovery state file to coordinate parallel research agents
- Research practical information, cultural context, and visitor experiences for all discovered options
- Generate comprehensive destination research catalogs with complete information
- Update TODO status and prepare research files for future itinerary planning

**Commands Available:**
- `/discovery [destination]` - Start discovery research for a destination
- `/research [destination]` - Conduct detailed research using discovery state

See `.claude/commands/` for detailed command specifications and workflows.

## State Files Management (`/research/state/`)

State files coordinate research workflow between discovery and detailed research phases. They contain prioritized locations using todo format (`- [ ]`) and research assignments for parallel agent deployment.

**File naming:** `{destination-slug}-discovery-state.md`
**Purpose:** Bridge between discovery and research phases with comprehensive findings and structured todo lists
**Management:** Created by `/discovery` command, used by `/research` command

See `.claude/commands/` for detailed state file structure and usage specifications.

## CLAUDE.md Maintenance Protocol

**Update Requirements**:
- **Mandatory**: Structural changes, new tools/resources, workflow modifications
- **Optional**: Minor content additions or template tweaks

**Update Process**:
1. **Always include "Update CLAUDE.md to reflect changes" as the final todo item** when creating any todo list for tasks involving structural changes
2. Focus on ensuring the generation process produces correct results rather than updating current test files
3. Keep templates and commands current and accurate
4. Maintain accuracy of file paths and directory structures

**What to Include**:
- Structural changes to folders, files, or organization
- New tools, resources, or external services
- Updated workflows, processes, or commands
- Template modifications and additions
- Timeline structure changes

**What NOT to Include**:
- Temporary project details or one-off research notes
- Specific trip dates or personal preferences
- Overly detailed implementation notes
- Content that becomes outdated quickly

This documentation serves as the definitive reference for the timeline-based Japan trip research project, ensuring consistency and continuity across all development iterations.