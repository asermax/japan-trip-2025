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

**Phase 1: Location Discovery (Parallel Agents)**
1. Deploy Location Scavenger Agent and Location Discovery Agent (gemini-based) in parallel with identical location prompts
2. Both agents work on the same discovery tasks: identifying sources, attractions, POIs, events, and related locations
3. Each agent uses their available research tools (WebSearch/trusted resources vs. gemini research capabilities)
4. Compare and merge results from both agents into unified comprehensive state file
5. Prioritize locations based on consolidated findings from both research approaches
6. Cross-reference findings between agents for validation and completeness
7. Generate integrated list for detailed research phase

**Phase 2: Detailed Research (Researcher)**
1. Reference the state file research assignments and priority tiers
2. Deploy Location Researcher Agents in parallel batches as defined in state file
3. Each agent researches specific locations with context from state file
4. Research practical information: hours, seasons, accessibility, costs, current status
5. Gather cultural context and visitor experiences using Gemini when needed
6. Document findings in structured format with priority tier and base recommendation status
7. Cross-reference findings between related locations for integration insights

**Phase 3: Content Organization**
1. Create destination-specific research file in `/research/destinations/`
2. Structure information by categories: attractions, food, logistics, culture
3. Include source citations and last-updated dates
4. Note seasonal considerations and booking requirements

**Phase 4: Validation and Documentation**
1. Cross-reference multiple sources for accuracy
2. Verify current operating status and requirements
3. Document research process and findings
4. Update TODO list status to reflect progress

## State Files Management (`/research/state/`)

The state folder contains intermediate files used during the research workflow to coordinate between different research phases and agents.

### State File Format

State files follow this naming convention: `{destination}-{phase}-state.md`

**Example:** `fujikawaguchiko-discovery-state.md`

### State File Structure

```markdown
# {Destination} - Discovery State

**Date:** {Creation date}
**Visit Period:** {Travel dates}
**Accommodation:** {Lodging details}
**Status:** {Current phase status}

## Comprehensive Research Findings

### Information Sources Discovered
- **Official Resources:** {Count and key sources from both agents}
- **Travel Guides:** {Major coverage found across research methods}
- **Community Resources:** {Forum/social platforms identified}
- **Media Resources:** {Video/photo content discovered}

### Cultural and Contextual Information
- **Cultural Significance:** {Key cultural insights and context}
- **Local Perspectives:** {Authentic experiences and recommendations}
- **Historical Background:** {Relevant historical context}
- **Regional Specialties:** {Local customs, traditions, and unique aspects}

## Priority Locations for Research

### Tier 1 - Essential
- {Location name} - {Brief description and significance}

### Tier 2 - Conditional
- {Location name} - {Conditions for inclusion and context}

### Tier 3 - Backup Options
- {Location name} - {Alternative option context and considerations}

## Date-Specific Events

### {Event/Festival name}
- **Period:** {Duration}
- **Locations:** {Where it occurs}
- **Features:** {What to expect}
- **Cultural Context:** {Significance and background}

## Base Recommendations Cross-Reference

### Already in Base Recommendations
- ✅ {Location name} - {Validation status and additional context}

### New Discoveries
- 🆕 {Location name} - {Significance and why it merits inclusion}

## Research Assignments

### Batch 1 - {Category}
- Agent A: {Locations/tasks with comprehensive context}
- Agent B: {Locations/tasks with integrated background}

## Follow-up Research Topics for Detailed Phase

### {Category}
- {Topic identified from comprehensive research findings}
```

### State File Usage

1. **Creation**: After parallel discovery agent research completion
2. **Compilation**: Merge findings from both Location Scavenger Agent and Location Discovery Agent
3. **Integration**: Combine complementary insights into unified comprehensive findings
4. **Validation**: Cross-reference findings between both research approaches for completeness
5. **Purpose**: Coordinate parallel research activities and provide context to researcher agents
6. **Reference**: Used by location researcher agents for task assignment and priority understanding
7. **Parallel Processing**: Research assignments enable multiple agents to work simultaneously
8. **Updates**: Modified as research phases progress to track completion status
9. **Cleanup**: Archived once final destination research is complete

### Parallel Research Execution

**Phase 1 - Discovery (Main Agent Orchestration):**
1. **Execute in parallel**: Deploy Location Scavenger Agent AND Location Discovery Agent with identical location prompts
2. **Wait for both results** before proceeding to compilation
3. **Compare findings**: Identify overlaps, unique discoveries, and complementary insights
4. **Compile state file**: Merge results into unified comprehensive findings without source differentiation
5. **Prioritize locations**: Use integrated findings from both practical accessibility and cultural significance perspectives

**Phase 2 - Detailed Research:**
1. **Read the compiled state file** to understand the full context and research assignments
2. **Deploy multiple Location Researcher Agents** simultaneously using the batch assignments
3. **Provide each agent with**:
   - Specific location(s) from their assigned batch
   - Priority tier context (Essential/Conditional/Backup)
   - Visit dates and accommodation information
   - Base recommendation status (existing vs. new discovery)
   - Cultural and contextual background from comprehensive discovery phase
   - Integrated research context from both discovery approaches
4. **Monitor parallel execution** and coordinate findings for integration insights
5. **Compile results** from all agents into comprehensive destination research

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