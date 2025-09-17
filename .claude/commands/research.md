# Detailed Location Research Command

This command conducts comprehensive detailed research on locations identified during discovery, deploying multiple Location Researcher Agents in parallel based on the research assignments from the discovery state file.

## Usage
```
/research [destination]
```

If no destination is provided, the command will automatically select the destination with the most recent discovery state file in `research/state/`.

## Prerequisites
- **Required**: Discovery must be completed
- **Required**: Discovery state file must exist: `research/state/{destination-slug}-discovery-state.md`
- **State file must contain**: Research assignments and priority locations in todo format

## Process Overview

### 1. Validation & Setup
1. **Destination Selection**:
   - **With argument**: Use provided destination and locate corresponding state file
   - **Without argument**: Find most recent `*-discovery-state.md` file in `research/state/`

2. **State File Validation**:
   - Verify discovery state file exists
   - **If missing**: Alert user and stop execution with message:
     ```
     ❌ Error: No discovery state file found for {destination}.
     Please run /discovery {destination} first to complete the discovery phase.
     ```
   - Parse state file for research assignments and context

3. **Extract Context from State File**:
   - Visit dates and accommodation details
   - Priority locations organized by tier
   - Cultural and contextual background
   - Research batch assignments
   - Date-specific events and festivals

### 2. Parallel Research Agent Deployment

Deploy **multiple Location Researcher Agents simultaneously** based on state file batch assignments:

**Agent Assignment Strategy:**
- **Batch 1**: Essential locations (Tier 1) - Deploy 2 agents in parallel
- **Batch 2**: Conditional locations (Tier 2) - Deploy 2 agents in parallel
- **Batch 3**: Backup options (Tier 3) - Deploy 1-2 agents based on list size

**Per-Agent Context Package:**
```
Research comprehensive information for your assigned locations in: {DESTINATION}

Visit Period: {VISIT_DATES} (for seasonal context and events reference)
Duration: {STAY_DURATION} (for planning context only)
Accommodation: {ACCOMMODATION_NAME} - {ACCOMMODATION_ADDRESS}

RESEARCH PURPOSE: Complete cataloging of all information about each assigned location.
This is NOT about fitting into a specific itinerary - research and document everything useful.

## Your Research Assignment
{SPECIFIC_LOCATIONS_FROM_BATCH}

## Background Context (from Discovery)
{CULTURAL_CONTEXT_FROM_STATE_FILE}
{DATE_SPECIFIC_EVENTS}
{INFORMATION_SOURCES_DISCOVERED}

## Research Focus Areas

**CRITICAL APPROACH**: Research each location as a SEPARATE ATTRACTION FILE. Every specific place to visit, dining experience, district exploration, or activity gets its own detailed file.

For each assigned location, research:

### Destination Summary Creation
- **Brief overview only** (2-3 paragraphs total for entire destination)
- Cultural significance and timing context
- One-sentence summaries for districts, food culture, day trips
- **NO detailed information** in destination file

### Individual Attraction Research (DETAILED)
For EVERY specific location discovered:

**Practical Information**
- Complete operating hours and seasonal schedules
- Full admission costs and booking requirements
- Detailed accessibility and transportation options
- Current operational status and any restrictions
- Optimal visiting times and crowd management strategies

**Cultural Context & Experience**
- Comprehensive cultural significance and historical background
- Complete visitor experience expectations
- Photography guidelines and cultural restrictions
- Detailed cultural etiquette and proper behavior protocols
- Local customs, traditions, and cultural preparation

**Visitor Experience**
- Recent visitor reviews and comprehensive experience reports
- Detailed duration recommendations and time considerations
- What makes this location special, unique, and worth visiting
- Connections with nearby locations and integration opportunities
- Comprehensive practical tips for international visitors

## Research Instructions
- **SEPARATE FILES**: Create individual attraction files for EVERY specific location, restaurant, district area, day trip, activity
- Use multiple research tools in parallel when possible
- Verify information across multiple sources
- **SOURCE CITATION**: Include inline source references immediately after relevant content
- **CITATION FORMAT**: Use `*Source: [Description](URL) - Accessed Date*` format
- Note seasonal considerations and optimal visiting conditions
- Cross-reference with cultural context from discovery phase
- Document all available information regardless of trip duration constraints
- Use Gemini research for cultural deep-dives when needed
- **Destination file**: Only summary information, all details go to attraction files
- **CITATION PLACEMENT**: Source each practical detail, cultural claim, and recommendation separately

## Output Format

**Destination File**: Brief summary only with:
- Cultural overview and significance (2-3 paragraphs) **with inline source citations**
- One-sentence district summaries **with source references**
- One-sentence food culture overview **with cultural source attribution**
- One-sentence day trip summaries **with source citations**

**Individual Attraction Files**: Comprehensive detail with:
- Complete practical visiting information **with sources for hours, costs, access details**
- Detailed cultural context and significance **with source references for historical claims**
- Full visitor experience expectations and recommendations **with source attribution**
- Integration notes with other regional attractions **with cross-reference sources**
- Comprehensive logistics and cultural preparation **with source citations for recommendations**
- **INLINE CITATIONS**: Source each section immediately after relevant content using `*Source: [Description](URL) - Accessed Date*` format
```

### 3. Research Coordination & Integration

**Parallel Execution Management:**
1. Launch all agent batches with their specific assignments
2. Monitor progress and coordinate cross-references between agents
3. Ensure agents can reference each other's findings for integration insights
4. Compile results maintaining priority tier context and base recommendation status

**Integration Points:**
- Cross-reference findings between related locations
- Identify timeline integration opportunities
- Note transportation connections and logical groupings
- Highlight seasonal considerations specific to visit dates

### 4. Results Compilation & Documentation

**State File Updates:**
1. Update existing state file with research completion status
2. Check off completed todo items in priority location lists:
   ```markdown
   ### Tier 1 - Essential
   - [x] {Location name} - {Research completed with key findings summary}
   - [ ] {Location name} - {Still pending research}
   ```

**Detailed Research Output:**
Create research files structured for timeline generation following the new destination/attraction separation:

1. **Main destination file:** `research/destinations/{destination-slug}.md` (SUMMARY ONLY)
2. **Destination attractions folder:** `research/attractions/{destination-slug}/` (CREATE DIRECTORY)
3. **Individual attraction files:** `research/attractions/{destination-slug}/{attraction-slug}.md` (DETAILED INFORMATION)

**Required Destination File Structure** (`research/destinations/[destination].md`):
```markdown
# {Destination} Research

**Visit Period:** {Visit dates}
**Duration:** {Stay duration}
**Accommodation:** {Name and address}
**Research Completed:** {Date}
**Discovery State:** research/state/{destination-slug}-discovery-state.md

## Basic Information
{2-3 paragraph overview covering cultural significance and timing context - SUMMARY ONLY}
*Source: [Cultural Source](URL) - Accessed Date*

## Key Districts & Neighborhoods
{Brief district summaries - 1 sentence each, no detailed information}
*Source: [District Source](URL) - Accessed Date*

## Food Culture
{Brief cuisine overview - 1-2 sentences each category, no detailed restaurant info}
*Source: [Food Culture Source](URL) - Accessed Date*

## Day Trips from {Destination}
{Brief day trip summaries - 1-2 sentences each, no detailed logistics}
*Source: [Day Trip Source](URL) - Accessed Date*
```

**Required Individual Attraction File Structure** (`research/attractions/[destination]/[attraction-slug].md`):
```markdown
# {Attraction Name} Research

**Location:** {Specific location within destination}
**Category:** {Attraction type}
**Cost:** {Entry fees or cost range}
**Best Time:** {Optimal visiting conditions}
**Duration:** {Recommended time allocation}
**Research Completed:** {Date}

## Basic Information
{DETAILED description, significance, and comprehensive overview}
*Source: [Source Name](URL) - Accessed Date*

## Cultural & Religious Significance
{DETAILED historical context, spiritual importance, and cultural practices}
*Source: [Cultural Source](URL) - Accessed Date*

## Visiting Information
{COMPLETE hours, costs, access, transportation, and current operational status}
*Source: [Official Source](URL) - Accessed Date*

## The Trail Experience
{DETAILED visitor experience, physical requirements, and complete journey description}
*Source: [Experience Source](URL) - Accessed Date*

## Practical Visiting Tips
{COMPREHENSIVE strategy, cultural preparation, optimal timing, and detailed logistics}
*Source: [Tips Source](URL) - Accessed Date*
```

**Critical File Generation Requirements:**
- **Destinations**: Summary-only files (max 50 lines total) **with inline source citations**
- **Attractions folder**: Create `research/attractions/{destination-slug}/` directory
- **Individual attractions**: EVERY specific place, restaurant, district, day trip, activity becomes a separate attraction file
- **Comprehensive detail**: ALL practical and cultural information goes in attraction files, not destination files
- **Attraction categories**: Include scenic locations, cultural sites, culinary experiences, transportation hubs, day trips, activity centers
- **SOURCE REQUIREMENTS**: All files must include inline source citations immediately after relevant content
- **CITATION FORMAT**: Use `*Source: [Description](URL) - Accessed Date*` format throughout all sections
- Structure must match `scripts/generate_timeline.py` expectations

## Logistics & Practical Information

### Transportation
{How to get around, key routes, transportation options}

### Food & Dining
{Notable restaurants, local specialties, dining customs}

### Accommodation Integration
{How location relates to lodging, nearby amenities}

### Weather & Seasonal Considerations
{Seasonal information and optimal visiting conditions}

## Regional Connections
{How locations connect within the region and complement each other}

## Research Process Notes
- **Discovery Agents Used:** Location Scavenger + Location Discovery (gemini)
- **Research Agents Deployed:** {Number} agents across {Number} batches
- **Sources Consulted:** {Primary source types}
- **Last Updated:** {Date}
- **Status:** Research completed, ready for future itinerary planning
```

### 5. TODO Status Update

Update destination status in `research/destinations-todo.md`:
- Change from "🔍 Research in progress" to "✅ Research completed"
- Add reference to completed research file

### 6. State File Completion

Update the discovery state file to reflect research completion:
- Mark all priority locations as researched: `- [x]`
- Add completion date and research file reference
- Update status to "Research completed"

## Success Criteria
- All priority locations researched by assigned agents
- Comprehensive destination research catalog created
- State file updated with completion status
- TODO file updated to reflect completed research
- Ready for future content generation and itinerary planning

## Error Handling

**Missing State File:**
```
❌ Error: Discovery state file not found for {destination}
Expected file: research/state/{destination-slug}-discovery-state.md

Please complete discovery first:
/discovery {destination}
```

**Incomplete State File:**
```
⚠️  Warning: State file exists but appears incomplete
Missing required sections: {missing_sections}

Please re-run discovery to generate complete state file.
```

## Output
The command should conclude with:
1. Summary of locations researched across all tiers
2. Path to comprehensive research file created
3. Confirmation that destination research is complete
4. Next recommended action: Research catalog ready for future itinerary planning and content generation

## Integration with Content Generation
The detailed research catalog serves as input for:
- Future itinerary planning and daily schedule creation
- `python scripts/generate_timeline.py` for timeline content creation (when ready)
- Place guide generation with comprehensive information
- Attraction page creation with cultural context and practical details