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
   - TODO list organized by category
   - Cultural research topics and seasonal considerations
   - Date-specific events and festivals

### 2. Simplified Batch Processing with File Updates

Process research using predefined 5-agent batches with **immediate file creation/updates after each batch**:

**Batch Processing Strategy:**
- **Automatic Batch Creation**: Research command automatically divides ALL TODO list items across 5-agent batches
- **Category-Based Selection**: Pick items from high-priority categories first (Cultural/Historic, Natural/Scenic, Traditional) then process extra topic categories (Cultural Research & Context, Events & Festivals, Practical Research Topics)
- **Mixed Batches**: Each batch contains up to 5 items total (locations + extra topics) assigned to 5 agents running in parallel
- **Sequential Batches**: Complete one batch before starting the next

**File Update Points:**
- After each batch completion, immediately create/update destination and attraction files
- Update state file with batch completion status and findings
- Maintain continuous availability of research progress

**Per-Agent Context Package:**
```
Research comprehensive information for your assigned items in: {DESTINATION}

Visit Period: {VISIT_DATES} (for seasonal context and events reference)
Duration: {STAY_DURATION} (for planning context only)
Accommodation: {ACCOMMODATION_NAME} - {ACCOMMODATION_ADDRESS}

RESEARCH PURPOSE: Complete cataloging of all information about each assigned item (locations + cultural/practical topics).
This is NOT about fitting into a specific itinerary - research and document everything useful.

## Your Research Assignment
{SPECIFIC_ITEMS_FROM_BATCH} (Mix of locations and cultural/practical research topics)

## Background Context (from Discovery)
{CULTURAL_RESEARCH_TOPICS}
{DATE_SPECIFIC_EVENTS}
{PRACTICAL_CONSIDERATIONS}

## Research Focus Areas

**CRITICAL APPROACH**:
- **Locations**: Research each location as a SEPARATE ATTRACTION FILE. Every specific place to visit, dining experience, district exploration, or activity gets its own detailed file.
- **Cultural/Practical Topics**: Research topics are integrated into destination summary and relevant attraction files as contextual information.

For each assigned item, research:

### Destination Summary Creation (Enhanced with Research Topics)
- **Brief overview only** (2-3 paragraphs total for entire destination)
- Cultural significance and timing context **incorporating researched cultural topics**
- One-sentence summaries for districts, food culture, day trips **with researched context**
- **Cultural Research Integration**: Weave findings from cultural research topics into appropriate sections
- **Practical Context Integration**: Include relevant practical research findings in destination context
- **NO detailed information** in destination file - details go to attraction files

### Individual Attraction Research (DETAILED + Enhanced Context)
For EVERY specific location discovered:

**Practical Information**
- Complete operating hours and seasonal schedules
- Full admission costs and booking requirements
- Detailed accessibility and transportation options
- Current operational status and any restrictions
- Optimal visiting times and crowd management strategies

**Cultural Context & Experience (Enhanced with Research Topics)**
- Comprehensive cultural significance and historical background **enhanced with researched cultural topics**
- Complete visitor experience expectations **informed by cultural research findings**
- Photography guidelines and cultural restrictions **with proper etiquette from practical research**
- Detailed cultural etiquette and proper behavior protocols **from researched customs and traditions**
- Local customs, traditions, and cultural preparation **incorporating relevant research topic findings**

**Visitor Experience**
- Recent visitor reviews and comprehensive experience reports
- Detailed duration recommendations and time considerations
- What makes this location special, unique, and worth visiting
- Connections with nearby locations and integration opportunities
- Comprehensive practical tips for international visitors

## Research Instructions
- **SEPARATE FILES**: Create individual attraction files for EVERY specific location, restaurant, district area, day trip, activity
- **TOPIC INTEGRATION**: Research topics enhance destination and attraction context but don't create separate files
- **Cultural Topics**: Integrate findings into destination cultural overview and relevant attraction cultural context
- **Practical Topics**: Integrate findings into destination practical considerations and attraction visiting tips
- Use multiple research tools in parallel when possible
- Verify information across multiple sources
- **SOURCE CITATION**: Include inline source references immediately after relevant content
- **CITATION FORMAT**: Use subtle `[🔗](URL)` format at the end of relevant paragraphs
- **IMAGE REQUIREMENTS**: Each research agent must include a representative image in their research report's Image section. The command will validate the image URL and integrate it into the final files
- **LOCATION PINS**: Add Google Maps location link at the end of each file: `**Location:** [View on Google Maps](google_maps_url)`
- **PHOTO SOURCING**: Search for official tourism photos, Wikipedia commons, or other freely available images that represent the location
- Note seasonal considerations and optimal visiting conditions
- Cross-reference with cultural context from discovery phase
- Document all available information regardless of trip duration constraints
- Use Gemini research for cultural deep-dives when needed
- **Research Topic Handling**: When assigned cultural research topics (e.g., "Mount Fuji worship traditions"), research the topic thoroughly and integrate findings into relevant destination/attraction sections
- **Event/Festival Research**: When assigned event/festival topics, research current details, cultural significance, and visitor impact for integration into destination context
- **Practical Topic Research**: When assigned practical topics (e.g., "transportation etiquette"), research comprehensively and integrate into destination practical sections and relevant attraction visiting tips
- **Destination file**: Only summary information, all details go to attraction files
- **CITATION PLACEMENT**: Source each practical detail, cultural claim, and recommendation separately using `[🔗](URL)` format

## Output Format

**Destination File**: Brief summary only with:
- **Image Integration**: Extract image from research agent reports and validate URL
- Cultural overview and significance (2-3 paragraphs) **with inline citations using [🔗](URL)**
- One-sentence district summaries **with citations using [🔗](URL)**
- One-sentence food culture overview **with citations using [🔗](URL)**
- One-sentence day trip summaries **with citations using [🔗](URL)**
- **Google Maps location link** at the end of the file

**Individual Attraction Files**: Comprehensive detail with:
- **Image Integration**: Extract image from research agent reports and validate URL
- Complete practical visiting information **with citations using [🔗](URL)**
- Detailed cultural context and significance **with citations using [🔗](URL)**
- Full visitor experience expectations and recommendations **with citations using [🔗](URL)**
- Integration notes with other regional attractions **with citations using [🔗](URL)**
- Comprehensive logistics and cultural preparation **with citations using [🔗](URL)**
- **INLINE CITATIONS**: Source each section immediately after relevant content using `[🔗](URL)` format
- **Google Maps location link** at the end of the file
```

### 3. Automated Batch Execution & File Management

**Batch Creation Logic:**
1. **Parse TODO List**: Extract all `- [ ]` items from state file by category (locations AND research topics)
2. **Category Order**: Process categories in the order they appear in the state file
3. **Sequential Selection**: Pick items from first category, then second category, etc., maintaining state file order within each category
4. **Mixed Item Assignment**: Assign up to 5 items total (mix of locations and research topics) per batch to 5 agents running in parallel
5. **Batch Sequence**: Complete each batch fully before starting the next

**Per-Batch Execution:**
1. **Deploy Agents**: Launch 5 Location Researcher Agents with current batch assignments (mix of locations and research topics)
2. **Process Results**: Compile findings from completed agents, integrating research topic findings into appropriate destination/attraction context
3. **Update Files**:
   - Create/update destination summary file: `research/destinations/{destination-slug}.md` (incorporating research topic findings)
   - Create/update attractions directory: `research/attractions/{destination-slug}/`
   - Create/update attraction files for current batch locations (enhanced with relevant research topic context)
4. **Update State**: Mark batch items (locations AND research topics) as completed `[x]` in state file
5. **Checkpoint**: Confirm files created/updated and available for use

**Integration Points (Applied Per Batch):**
- Cross-reference findings between related locations discovered in current and previous batches
- Identify timeline integration opportunities as information becomes available
- Note transportation connections and logical groupings emerging from research
- Highlight seasonal considerations specific to visit dates in each batch

### 4. Incremental File Management & Updates

**Per-Batch State File Updates:**
After each batch completion, update the state file to reflect progress:
```markdown
### {Category Name}
- [x] {Location name} - Research completed, attraction file created
- [x] {Location name} - Research completed, attraction file created
- [ ] {Location name} - Pending next batch research
```

**Incremental File Creation:**
Files are created and updated throughout the process:

**After Each Batch:**
1. **Update destination file:** `research/destinations/{destination-slug}.md` - Add any new context discovered
2. **Create/update attractions directory:** `research/attractions/{destination-slug}/`
3. **Create attraction files:** `research/attractions/{destination-slug}/{attraction-slug}.md` for each researched location
4. **Cross-reference updates:** Add connections discovered between current and previous batch locations

**Required Destination File Structure** (`research/destinations/[destination].md`):
```markdown
# {Destination} Research

**Visit Period:** {Visit dates}
**Duration:** {Stay duration}
**Accommodation:** {Name and address}
**Research Completed:** {Date}
**Discovery State:** research/state/{destination-slug}-state.md

## Basic Information

![Destination overview image](image_url)
*Caption: {Brief description of the image}*

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

**Location:** [View on Google Maps](google_maps_url)
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

![Attraction image](image_url)
*Caption: {Brief description of the image}*

{DETAILED description, significance, and comprehensive overview}
*Source: [Source Name](URL) - Accessed Date*

## Cultural & Religious Significance
{DETAILED historical context, spiritual importance, and cultural practices}
*Source: [Cultural Source](URL) - Accessed Date*

## Visiting Information
{COMPLETE hours, costs, access, transportation, and current operational status}
*Source: [Official Source](URL) - Accessed Date*

## The Experience
{DETAILED visitor experience, physical requirements, and complete journey description}
*Source: [Experience Source](URL) - Accessed Date*

## Practical Visiting Tips
{COMPREHENSIVE strategy, cultural preparation, optimal timing, and detailed logistics}
*Source: [Tips Source](URL) - Accessed Date*

**Location:** [View on Google Maps](google_maps_url)
```

**Critical File Generation Requirements:**
- **Destinations**: Summary-only files (max 50 lines total) **with inline source citations, representative photo, and Google Maps link**
- **Attractions folder**: Create `research/attractions/{destination-slug}/` directory
- **Individual attractions**: EVERY specific place, restaurant, district, day trip, activity becomes a separate attraction file
- **Comprehensive detail**: ALL practical and cultural information goes in attraction files, not destination files
- **Attraction categories**: Include scenic locations, cultural sites, culinary experiences, transportation hubs, day trips, activity centers
- **PHOTO REQUIREMENTS**: Every destination and attraction file must include at least one representative photo using markdown format
- **LOCATION REQUIREMENTS**: Every file must include Google Maps location link at the end
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

### 5. Per-Batch Progress Updates

**After Each Batch:**
1. **Update State File**: Mark completed locations with `- [x]` and note files created
2. **Update Progress Status**: Indicate which batch is completed and files available
3. **Checkpoint Confirmation**: Confirm files are accessible and properly structured

**TODO Status Updates:**
- **After Final Batch**: Update status to "✅ Research completed"

### 6. Final State File Completion

After all batches complete, finalize the discovery state file:
- Mark all priority locations as researched: `- [x]`
- Add completion date and research file reference
- Update status to "Research completed"
- Add summary of all files created throughout the process

## Success Criteria
- **Per-Batch Success**: After each batch, files are created/updated and available for use
- **Incremental Progress**: Research findings accessible throughout the process
- **State File Tracking**: Continuous updates showing completed vs. pending research
- **File Availability**: Destination and attraction files updated after each batch
- **Final Completion**: All priority locations researched and comprehensive catalog created
- **TODO Tracking**: Granular progress updates showing batch completion status
- **Ready for Use**: Research files available for content generation and itinerary planning throughout process

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

**Per-Batch Output:**
After each batch completion, provide:
1. **Batch Summary**: Locations researched in current batch
2. **Files Created/Updated**: Specific file paths created or modified
3. **Progress Status**: Which tiers completed, which remain
4. **Next Batch**: Preview of upcoming research batch

**Final Output:**
After all batches complete, provide:
1. **Complete Summary**: All locations researched across all tiers
2. **Full File Catalog**: All destination and attraction files created
3. **Research Completion**: Confirmation that destination research is complete
4. **Availability**: Research catalog ready for immediate use in content generation and itinerary planning

## Integration with Content Generation
The detailed research catalog serves as input for:
- Future itinerary planning and daily schedule creation
- `python scripts/generate_timeline.py` for timeline content creation (when ready)
- Place guide generation with comprehensive information
- Attraction page creation with cultural context and practical details