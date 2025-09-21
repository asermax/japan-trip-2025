# Japan Trip 2025 Research Project

This project is designed to research, organize, and present information about our upcoming Japan trip using AI tools and Zola static site generator with a **timeline-based approach**.

## Project Structure

```
japan-trip-2025/
   research/               # Raw research data and notes
      destinations/       # City/town research
      routes/            # Car route research organized by route folder
         {route-name}/   # Individual route folders (main-route, coastal-route, etc.)
      attractions/       # POI research organized by destination/route folders
         {destination}/  # Destination-specific attractions
         {route-name}/   # Route-specific stops and attractions
      state/             # Intermediate state files for research workflow
         {destination}-state.md        # Destination discovery states
         {origin-to-destination}-{route-name}-route-state.md # Route discovery states
      destinations-todo.md # Destination research tracking
      routes-todo.md     # Route research tracking
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
1. Structure research files according to timeline generator requirements (see Research File Structure below)
2. Run `python scripts/generate_timeline.py` to generate content from research files
3. Script automatically creates timeline entries, place guides, and attraction pages
4. All content follows consistent frontmatter templates
5. Cross-linking between timeline, places, and attractions handled automatically
6. Source citations maintained from research files

#### Research File Structure for Content Generation

**Destination Research Files** (`research/destinations/[destination].md`)
Must include these sections for proper timeline generation - **DESTINATIONS SHOULD BE SUMMARIES ONLY**:
- `## Basic Information` - Overview and cultural significance (2-3 paragraphs max) **with source citations for cultural claims**
- `## Key Districts & Neighborhoods` - Brief district summaries (1 sentence each) **with source references**
- `## Food Culture` - Brief cuisine overview (1-2 sentences each category) **with cultural source attribution**
- `## Day Trips from [destination]` - Brief day trip summaries (1-2 sentences each) **with source citations**

**Individual Attraction Files** (`research/attractions/[destination]/[attraction-slug].md`)
**ATTRACTIONS CONTAIN ALL DETAILED INFORMATION** - organized by destination folder:
- `## Basic Information` - Detailed description, significance, and comprehensive overview **with inline source citations**
- `## Cultural & Religious Significance` - Historical and cultural context with deep detail **with source references for historical claims**
- `## Visiting Information` - Hours, costs, access details, operating information **with sources for practical details**
- `## The Trail Experience` - Complete visitor experience description **with source attribution for experience details**
- `## Practical Visiting Tips` - Detailed strategy, cultural preparation, logistics **with source citations for recommendations**

**Attraction Categories** (all experiences should be individual attractions):
- **Scenic locations** - Parks, viewpoints, districts, natural areas
- **Cultural sites** - Temples, shrines, heritage centers, museums
- **Culinary experiences** - Traditional cuisine, modern dining, food culture
- **Transportation hubs** - Station areas, central districts with logistics
- **Day trip destinations** - Extended cultural experiences, nearby locations
- **Activity centers** - Observation facilities, craft workshops, cultural activities

**Example Research Command Output:**
The `/research [destination]` command should generate:
1. Main destination file: `research/destinations/fujikawaguchiko.md` (summary only)
2. Destination attractions folder: `research/attractions/fujikawaguchiko/`
3. Individual attraction files: `research/attractions/fujikawaguchiko/chureito-pagoda.md`, etc.
4. Updated state files with completion status
5. Updated TODO tracking with research completion status

**Key Principle**: Every specific place to visit, dining experience, district exploration, or activity should be a separate attraction file. Destinations provide only cultural context and brief overviews.

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

### Task Automation
```bash
# Automated task processing
./run_tasks.sh           # Start task processing immediately
./run_tasks.sh 30        # Start with 30-minute delay

# Task management
# Place .md files with claude commands in tasks/pending/
# Completed tasks automatically moved to tasks/completed/ with results
# Failed tasks retried up to 3 times before skipping
# Cycles run every 5 hours with accurate timing
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
- Conducts detailed research on locations identified by scavenger and returns comprehensive reports
- Uses multiple research tools in parallel when possible
- Verifies practical information (hours, costs, accessibility, current status)
- Researches cultural context and visitor experiences
- **Returns detailed reports** that the main research command processes to create destination and attraction files

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
4. **Maintain source citations in proper format with inline references**
5. **Include source links close to referenced content in final files**
6. Update CLAUDE.md when workflows or tools change

### Source Citation Requirements

**Inline Source References:**
- Include source links immediately after relevant content sections
- Use format: `[🔗](URL)` for subtle, clickable source links
- Place citations at paragraph or section level, not just at document end
- For multiple sources in one section, list all relevant sources

**Citation Placement:**
- **Destinations**: Source each cultural claim, historical fact, and practical detail
- **Attractions**: Source visiting information, cultural significance, and practical tips separately
- **Research Files**: Maintain source tracking throughout research process

**Citation Format Examples:**
```markdown
The site achieved National Natural Monument status in 1934 and became part of the Mount Fuji UNESCO World Heritage Site in 2013. [🔗](https://whc.unesco.org/en/list/1418/)

**Operating Hours:** 9:00 AM - 5:00 PM daily [🔗](https://example.com)

Traditional houtou noodles represent the region's mountain survival cuisine. [🔗](https://example.com)
```

### Image Validation Requirements

**Image Source Validation:**
- Agents must extract valid image URLs from websites they research OR perform separate image searches
- Agents must NOT construct or guess image URLs themselves
- All images must be from legitimate sources visited during research (official websites, tourism boards, Wikipedia) or found through dedicated image searches
- Research commands validate image URLs from agent reports before including in final files

**Acceptable Image Sources:**
- Official tourism sites and government pages
- Wikipedia and Wikimedia Commons
- Established travel websites with proper image sourcing
- Official venue/attraction websites

**Image Requirements in Research Reports:**
- Extract images directly from researched sources
- Verify image URLs are valid and accessible
- Provide source attribution in image captions
- Include representative images that accurately depict the location/attraction

### Destination Research Methodology

**Research Purpose:** Comprehensive cataloging of all available options, attractions, and experiences for each destination with **strict separation of concerns**. This is **not** itinerary planning - the goal is to research and document everything worth knowing for later reference and decision-making.

**CRITICAL STRUCTURE PRINCIPLE:**
- **Destinations** = Cultural context and brief summaries only
- **Attractions** = ALL specific places, experiences, districts, restaurants, activities, day trips

The research process consists of two main phases:

**Discovery Phase** (`/discovery [destination]`)
- Deploy parallel agents to identify all information sources and potential attractions
- Generate comprehensive state file with all discovered options organized by interest/significance
- Cross-reference base recommendations with new discoveries
- Create research assignments for detailed investigation of all options

**Detailed Research Phase** (`/research [destination]`)
- **Enhanced Batch Processing**: Research using predefined 3-agent batches processing both attractions AND research topics
- **Agent Role**: Agents conduct research and return comprehensive reports (do NOT create files directly)
- **Main Command Role**: Processes agent reports and creates/updates destination and attraction files
- **Automatic Batch Creation**: Command divides ALL TODO list items (attractions + cultural/practical topics) across 3-agent batches based on state file order
- **Sequential Processing**: Process categories in state file order, up to 3 items total (mixed attractions and research topics) per batch
- **Topic Integration**: Cultural and practical research topics enhance destination and attraction context rather than creating separate files
- **Immediate File Updates**: Create/update destination and attraction files after each batch completion with integrated research topic findings
- **Continuous Availability**: Research files accessible throughout the process for immediate use
- Update TODO status and state file after each batch completion

**Commands Available:**
- `/discovery [destination]` - Start discovery research for a destination
- `/research [destination]` - Conduct detailed research using discovery state

See `.claude/commands/` for detailed command specifications and workflows.

### Route Research Methodology

**Research Purpose:** Comprehensive cataloging of all available stops, attractions, and experiences along car routes between destinations. This is **not** itinerary planning - the goal is to research and document everything worth knowing about route options for later reference and decision-making.

The route research process consists of two main phases, parallel to destination research:

**Route Discovery Phase** (`/discover-route [from] [to]`)
- Deploy parallel agents to identify all driving route information sources and potential stops
- **Multiple Route Discovery**: Identify distinct route options (main highway, scenic alternatives, etc.)
- **Separate State Files**: Generate individual state files for each route option discovered
- **Per-Route TODO Lists**: Each route gets its own TODO list organized by detour level
- Create foundation for individual route research processing

**Detailed Route Research Phase** (`/research-route [route-state-file]`)
- **Individual Route Processing**: Research one specific route at a time using its state file
- **Enhanced Batch Processing**: Research using predefined 3-agent batches per route processing both stops AND research topics
- **Agent Role**: Agents conduct research and return comprehensive reports (do NOT create files directly)
- **Main Command Role**: Processes agent reports and creates/updates route and attraction files
- **Route-Specific File Structure**: Create separate folders and files for each route
- **Detour-Based Processing**: Process categories in state file order (On-Route → Short Detour → Major Detour → Cultural Research & Context → Route Events & Seasonal Factors → Practical Route Research Topics)
- **Topic Integration**: Cultural and practical research topics enhance route overview and stop context rather than creating separate files
- **Per-Route Output**: Generate route-specific research files and attraction catalogs with integrated research topic findings

**Commands Available:**
- `/discover-route [from] [to]` - Start discovery research for a car route (creates multiple route state files)
- `/research-route [route-state-file]` - Research a specific route using its individual state file

**Route Categories:**
- **On-Route Stops**: No detour required, directly accessible from main route
- **Short Detour Stops**: 15-30 minutes off main route
- **Major Detour Stops**: 30+ minutes off main route, significant cultural/scenic value

**Route TODO Management:** Track progress in `research/routes-todo.md` with all car journeys between destinations.

See `.claude/commands/` for detailed route command specifications and workflows.

## State Files Management (`/research/state/`)

State files coordinate research workflow between discovery and detailed research phases. They contain a comprehensive TODO list organized by category using todo format (`- [ ]`) for 3-agent batch processing, including both attractions/stops AND research topics.

**Destination State Files:**
- **File naming:** `{destination-slug}-discovery-state.md`
- **Purpose:** Bridge between destination discovery and research phases with TODO list organized by category (attractions + cultural/practical research topics)
- **Content:** Attraction locations AND cultural research topics, events/festivals, practical research topics
- **Management:** Created by `/discovery` command, used by `/research` command

**Route State Files:**
- **File naming:** `{origin-to-destination}-{route-name}-route-state.md`
- **Purpose:** Individual state files per route option with TODO list organized by detour level AND research topics
- **Content:** Route stops AND cultural research topics, route events/seasonal factors, practical route research topics
- **Multiple Files:** Discovery creates separate files for each route discovered (main, coastal, mountain, etc.)
- **Management:** Created by `/discover-route` command, individually used by `/research-route` command

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