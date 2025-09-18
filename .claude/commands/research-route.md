# Detailed Route Research Command

This command conducts comprehensive detailed research on stops and attractions identified during route discovery, deploying multiple Location Researcher Agents in parallel based on the research assignments from the route discovery state file.

## Usage
```
/research-route [route-state-file]
```

Examples:
- `/research-route tokyo-to-kyoto-main-route` - Research the main route
- `/research-route tokyo-to-kyoto-coastal-route` - Research the coastal alternative

If no route is provided, the command will list all available route state files and prompt for selection.

## Prerequisites
- **Required**: Route discovery must be completed
- **Required**: Individual route state file must exist: `research/state/{route-state-filename}.md`
- **State file must contain**: TODO list with priority stops organized by detour level

## Process Overview

### 1. Validation & Setup
1. **Route Selection**:
   - **With argument**: Use provided route state filename and locate corresponding state file
   - **Without argument**: List all available `*-route-state.md` files in `research/state/` and prompt for selection

2. **State File Validation**:
   - Verify individual route state file exists
   - **If missing**: Alert user and stop execution with message:
     ```
     ❌ Error: No route state file found: {route-state-filename}.md
     Available route state files: {list of available files}
     Please run /discover-route {from} {to} first to complete the discovery phase.
     ```
   - Parse state file for TODO list and route context

3. **Extract Context from State File**:
   - Travel date and route context
   - TODO list organized by detour level
   - Route options and cultural research topics
   - Route-specific considerations and seasonal factors

### 2. Simplified Batch Processing with File Updates

Process research using predefined 5-agent batches with **immediate file creation/updates after each batch**:

**Batch Processing Strategy:**
- **Automatic Batch Creation**: Research command automatically divides ALL TODO list items across 5-agent batches
- **Detour-Based Selection**: Pick items from categories in state file order (On-Route → Short Detour → Major Detour → Cultural Research & Context → Route Events & Seasonal Factors → Practical Route Research Topics)
- **Mixed Batches**: Each batch contains up to 5 items total (stops + research topics) assigned to 5 agents running in parallel
- **Sequential Batches**: Complete one batch before starting the next

**File Update Points:**
- After each batch completion, immediately create/update route research files
- Update state file with batch completion status and findings
- Maintain continuous availability of research progress

**Per-Agent Context Package:**
```
Research comprehensive information for your assigned items along the route: {ORIGIN} to {DESTINATION}

Travel Date: {TRAVEL_DATE} (for seasonal context and route conditions)
Transportation: Car/driving
Route Context: {ROUTE_DESCRIPTION_FROM_STATE}

RESEARCH PURPOSE: Complete cataloging of all information about each assigned item (stops + cultural/practical topics).
This is NOT about fitting into a specific itinerary - research and document everything useful.

**CRITICAL**: You will RETURN a detailed research report. You do NOT create files. The main command will process your report and create the appropriate route and attraction files.

## Your Research Assignment
{SPECIFIC_ITEMS_FROM_BATCH} (Mix of stops and cultural/practical research topics)

## Background Context (from Route Discovery)
{CULTURAL_RESEARCH_TOPICS}
{ROUTE_SPECIFIC_EVENTS_AND_CONSIDERATIONS}
{PRACTICAL_ROUTE_CONSIDERATIONS}

## Research Focus Areas

**CRITICAL APPROACH**:
- **Route Stops**: Research each stop thoroughly and provide comprehensive details in your report that will become individual attraction files
- **Cultural/Practical Topics**: Research topics thoroughly and provide findings that will be integrated into route overview and relevant stop context

For each assigned item, research:

### Practical Route Information
- Current operating hours and seasonal schedules
- Parking availability and accessibility from route
- Admission costs and booking requirements
- Current operational status (open/closed/renovations)
- Time needed for visit and route impact
- Distance from main route and detour time

### Route-Specific Context & Experience (Enhanced with Research Topics)
- Why this stop is significant for this specific route **enhanced with researched cultural topics**
- What to expect as a driving visitor **informed by cultural research findings**
- Photography opportunities and scenic viewpoints **with cultural context from research**
- Route-specific cultural significance **incorporating relevant research topic findings**
- Connection with route's overall journey narrative **enhanced by cultural and practical research**

### Driving Visitor Experience
- Recent visitor reviews focusing on route travelers
- Recommended visit duration for route travelers
- What makes this stop special for car travelers
- Connections with other stops along the route
- Practical tips for driving visitors (parking, access, facilities)

### Route Integration
- How this stop fits into the overall route experience
- Logical grouping with other route stops
- Seasonal considerations specific to travel date
- Alternative options if stop is unavailable

## Research Instructions
- **RETURN COMPREHENSIVE REPORTS**: Provide detailed findings for all assigned items in your research report
- **ROUTE STOP RESEARCH**: For every specific stop, rest area, scenic point along route - provide comprehensive details that will become individual attraction files
- **TOPIC INTEGRATION**: Research topics should be thoroughly researched with findings that will enhance route overview and stop context
- **Cultural Topics**: Provide comprehensive findings that will be integrated into route cultural overview and relevant stop cultural context
- **Practical Topics**: Provide detailed research that will be integrated into route practical considerations and stop driving tips
- **Route Research Topic Handling**: When assigned route cultural research topics (e.g., "traditional travel patterns"), research thoroughly and provide findings for integration into relevant route/stop sections
- **Event/Festival Research**: When assigned route event/festival topics, research current details and visitor impact
- **Practical Route Topic Research**: When assigned practical topics (e.g., "driving customs"), research comprehensively for integration into route overview and stop visiting tips
- Use multiple research tools in parallel when possible
- Verify information across multiple sources
- **IMAGE REQUIREMENTS**: Include a representative image URL and description in your research report for each route/stop researched
- **LOCATION PINS**: Include Google Maps location links in your research report
- **PHOTO SOURCING**: Find official tourism photos, Wikipedia commons, or other freely available images that represent the route/stop
- Note seasonal considerations and optimal visiting conditions for route
- Cross-reference with route context from discovery phase
- Document all available information regardless of detour time constraints
- Focus on car accessibility and driving visitor experience
- Use existing location researcher capabilities adapted for route context
- **COMPREHENSIVE REPORTING**: Provide all findings in your research report - the main command will organize information into route overviews and detailed stop files

## Agent Report Processing

**Agent Reports**: Agents return comprehensive research reports containing:
- Detailed findings for all assigned stops and research topics
- Source citations and URLs for all information
- Representative images and descriptions for route/stops
- Google Maps location links
- Route-specific context and practical information
- Integration suggestions and connections

**Main Command File Creation**: The research command processes agent reports to create route and stop files with proper formatting and citations.
```

### 3. Automated Batch Execution & File Management

**Batch Creation Logic:**
1. **Parse TODO List**: Extract all `- [ ]` items from state file by category (stops AND research topics)
2. **Category Order**: Process categories in state file order (On-Route → Short Detour → Major Detour → Cultural Research & Context → Route Events & Seasonal Factors → Practical Route Research Topics)
3. **Sequential Selection**: Pick items from first category, then second category, etc., maintaining state file order within each category
4. **Mixed Item Assignment**: Assign up to 5 items total (mix of stops and research topics) per batch to 5 agents running in parallel
5. **Batch Sequence**: Complete each batch fully before starting the next

**Per-Batch Execution:**
1. **Deploy Agents**: Launch 5 Location Researcher Agents with current batch assignments (mix of stops and research topics)
   - **Agent Role**: Research thoroughly and return detailed reports (agents do NOT create files)
   - **Main Command Role**: Process agent reports and create/update files based on findings
2. **Process Agent Reports**:
   - Receive detailed research reports from each agent
   - Integrate research topic findings into appropriate route/stop context
   - Extract images and source citations from agent reports
   - Validate URLs and practical information
3. **Create/Update Files** (Main Command Responsibility):
   - Create/update route research file: `research/routes/{route-name}/{origin-to-destination}-{route-name}.md` (incorporating research topic findings)
   - Create/update route attractions folder: `research/attractions/{route-name}/`
   - Create attraction files for route-specific stops: `research/attractions/{route-name}/{stop-slug}.md` (enhanced with relevant research topic context)
   - Add proper source citations, images, and Google Maps links to all files
4. **Update State**: Mark batch items (stops AND research topics) as completed `[x]` in state file
5. **Checkpoint**: Confirm files created/updated and available for use

**Route Integration Points (Applied Per Batch):**
- Cross-reference findings between related stops discovered in current and previous batches
- Identify logical stop groupings and route flow optimization
- Note seasonal considerations specific to travel date
- Highlight route-specific cultural or scenic connections

### 4. Incremental File Management & Updates

**Per-Batch State File Updates:**
After each batch completion, update the state file to reflect progress:
```markdown
### On-Route (No Detour)
- [x] {Stop name} - Research completed, route file updated
- [x] {Stop name} - Research completed, route file updated
- [ ] {Stop name} - Pending next batch research
```

**Incremental File Creation:**
Files are created and updated throughout the process:

**After Each Batch:**
1. **Update route research file:** `research/routes/{route-name}/{origin-to-destination}-{route-name}.md` - Add new stops researched
2. **Create/update route attractions:** Individual attraction files in `research/attractions/{route-name}/`
3. **Cross-reference updates:** Add connections discovered between current and previous batch stops

**Detailed Research Output:**
Create comprehensive research files:
- **Route Overview:** `research/routes/{route-name}/{origin-to-destination}-{route-name}.md`
- **Route Attractions:** `research/attractions/{route-name}/{stop-slug}.md` (individual files per stop)

**Required Route Overview File Structure** (`research/routes/{route-name}/{origin-to-destination}-{route-name}.md`):
```markdown
# {Origin} to {Destination} - {Route Name} Route Research

![Route overview image](image_url)
*Caption: {Brief description of the route image}*

**Travel Date:** {Travel date}
**Transportation:** Car/driving
**Route Type:** {Main/Scenic/Coastal/Mountain/etc.}
**Route Distance:** {Approximate distance and drive time}
**Research Completed:** {Date}
**Discovery State:** research/state/{origin-to-destination}-{route-name}-route-state.md

## Route Overview

**Primary Route:** {Main highway/road route}
**Alternative Scenic Routes:** {Alternative routes discovered}
**Estimated Drive Time:** {Base drive time without stops}

## On-Route Stops (No Detour)

### {Stop Name}
- **Type:** {Rest area/town/attraction/scenic viewpoint}
- **Location:** {Highway/road marker or town name}
- **Facilities:** {Parking, restrooms, food, etc.}
- **Visit Duration:** {Recommended time for stop}
- **Accessibility:** {Ease of access from route}

**Route Significance:** {Why this stop matters for this route}

**Driving Visitor Experience:** {What to expect, facilities, tips}

**Route Integration:** {How this fits with overall journey}

**Sources:** {Citations and verification dates}

---

## Short Detour Stops (15-30 minutes)

### {Stop Name}
- **Detour Time:** {Additional time from main route}
- **Type:** {Attraction/cultural site/scenic area}
- **Cost:** {Free/¥XXX}
- **Hours:** {Operating schedule}
- **Parking:** {Availability and cost}
- **Visit Duration:** {Recommended time}

**Route Context:** {Why worth the detour on this route}

**Driving Visitor Experience:** {What to expect, access, tips}

**Route Integration:** {Connection with other stops, route flow}

**Sources:** {Citations and verification dates}

---

## Major Detour Stops (30+ minutes)

### {Stop Name}
- **Detour Time:** {Additional time from main route}
- **Significance:** {Why this justifies major detour}
- **Type:** {Major attraction/cultural center/natural site}
- **Cost:** {Free/¥XXX}
- **Hours:** {Operating schedule}
- **Accessibility:** {Detailed access information}
- **Visit Duration:** {Recommended time}

**Route Justification:** {Why this major detour is worthwhile}

**Driving Visitor Experience:** {Comprehensive visitor information}

**Route Integration:** {Impact on overall journey, alternatives}

**Sources:** {Citations and verification dates}

---

## Route-Specific Considerations

### Seasonal Factors (for Travel Date)
{Weather conditions, road conditions, seasonal attractions}

### Traffic and Timing
{Best departure times, traffic patterns, peak periods}

### Fuel and Services
{Service areas, fuel stations, facilities along route}

### Cultural Route Context
{Cultural significance of the route, regional transitions, traditional travel patterns}

## Route Flow Recommendations

### Suggested Stop Combinations
{Logical groupings of stops that work well together}

### Alternative Route Strategies
{Different approaches based on interests, time constraints, weather}

### Route Integration with Destinations
{How route stops connect with origin and destination activities}

## Research Process Notes
- **Discovery Agents Used:** Route Scavenger + Route Discovery (gemini)
- **Research Agents Deployed:** {Number} agents across {Number} batches
- **Sources Consulted:** {Primary source types for route research}
- **Last Updated:** {Date}
- **Status:** Route research completed, ready for future itinerary planning

**Location:** [View route on Google Maps](google_maps_route_url)
```

**Required Route Stop/Attraction File Structure** (`research/attractions/{route-name}/{stop-slug}.md`):
```markdown
# {Stop Name} - {Route Name} Route Research

![Stop image](image_url)
*Caption: {Brief description of the stop image}*

**Route:** {Origin} to {Destination} - {Route Name}
**Detour Level:** {On-Route/Short Detour/Major Detour}
**Location:** {Specific location details}
**Type:** {Rest area/town/attraction/scenic viewpoint}
**Cost:** {Entry fees or cost range}
**Visit Duration:** {Recommended time for stop}
**Research Completed:** {Date}

## Basic Information
{DETAILED description, significance, and comprehensive overview from route perspective}
[🔗](URL)

## Route Context & Accessibility
{DETAILED route-specific context, parking, accessibility from route}
[🔗](URL)

## Driving Visitor Experience
{COMPLETE visitor experience for car travelers, facilities, what to expect}
[🔗](URL)

## Route Integration
{How this stop fits into overall route, connections with other stops, timing considerations}
[🔗](URL)

## Practical Driving Tips
{COMPREHENSIVE strategy for car travelers, parking, optimal timing, route impact}
[🔗](URL)

**Location:** [View on Google Maps](google_maps_url)
```

### 5. TODO Status Update

Update route status in `research/routes-todo.md`:
- Change from "🔍 Research in progress" to "✅ Research completed"
- Add reference to completed route research file

### 6. State File Completion

Update the route discovery state file to reflect research completion:
- Mark all priority stops as researched: `- [x]`
- Add completion date and research file reference
- Update status to "Research completed"

## Success Criteria
- All priority stops researched by assigned agents
- Comprehensive route research catalog created
- State file updated with completion status
- TODO file updated to reflect completed route research
- Ready for future content generation and itinerary planning

## Error Handling

**Missing State File:**
```
❌ Error: Route discovery state file not found for {origin-to-destination}
Expected file: research/state/{origin-to-destination}-route-discovery-state.md

Please complete route discovery first:
/discover-route {from} {to}
```

**Incomplete State File:**
```
⚠️  Warning: State file exists but appears incomplete
Missing required sections: {missing_sections}

Please re-run route discovery to generate complete state file.
```

## Output
The command should conclude with:
1. Summary of stops researched across all detour levels
2. Path to comprehensive route research file created
3. Confirmation that route research is complete
4. Next recommended action: Route catalog ready for future itinerary planning and content generation

## Integration with Content Generation
The detailed route research catalog serves as input for:
- Future itinerary planning and route scheduling
- `python scripts/generate_timeline.py` for timeline content creation (when ready)
- Journey page generation with comprehensive route information
- Attraction page creation for route-specific stops with driving context